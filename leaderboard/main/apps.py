from django.apps import AppConfig
from django.conf import settings
import time, schedule
from threading import Thread
import docker
import os
import re
import logging

SUBMISSIONS_PROCESSING = False

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if not os.environ.get('RUN_MAIN'):
            return
        # self.job()
        t = Thread(target= self.scheduler)
        t.daemon = True
        t.start() ## not using t.join() because it will block server

    @classmethod
    def scheduler(cls):
        schedule.every(10).seconds.do(cls.job)
        # schedule.every(1).minutes.do(cls.reset_requests_queue)

        # if settings.PRODUCTION: #spam ip detection and change for verifier
        #     schedule.every(3).minutes.do(test_spam)
        
        while True:
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def job(cls):
        global SUBMISSIONS_PROCESSING
        if SUBMISSIONS_PROCESSING:
            print('Task is Already Running !')
            return
        else:
            SUBMISSIONS_PROCESSING = True
            
            from main.models import Submission
            
            submissions_to_process = Submission.objects.filter(status = 'IN-QUEUE')
            for submission in submissions_to_process:
                print(f'Running Submission {submission}')
                try:
                    cls.run_container(submission)
                    submission.status = 'DONE'
                    submission.save()
                except Exception as e:
                    submission.status = 'ERROR'
                    submission.save()
                    print(e)
                    logging.exception(e)
                    print('Failed to process submission', submission)
            
            SUBMISSIONS_PROCESSING = False

    @classmethod
    def run_container(cls, submission):
        time.sleep(10)

        client = docker.from_env()
        
        image = submission.challenge.processor.image_name.strip()
        command = submission.challenge.processor.command.split(image)[1].strip()

        print('Reading Mounts')
        mounts, original_paths, processed_paths = cls.create_mounts(submission)

        command = cls.process_command_paths(command, original_paths, processed_paths)

        print('Launching Container')
        results = client.containers.run(
            image, 
            command,
            mounts = mounts,
            auto_remove = True,
        )

        results = results.decode("utf-8")
        print(results)
        logging.debug(results)

        score = results.split('Score is:')[1].split('\n')[0].strip()
        print(f"Extracted Score {score}")

        submission.score = float(score)
        submission.save()


    @classmethod
    def create_mounts(cls, submission):
        mounts = []
        original_paths = []
        processed_paths = []

        args = submission.challenge.processor.command.split(' ')
        for i, arg in enumerate(args):
            if args[i].strip() != '-v':
                continue

            source, target = args[i+1].split(':')
            original_paths += [source, target]

            print(source, target)

            source = cls.process_mount_path(submission, source)
            target = cls.process_mount_path(submission, target)

            print(source, target)

            if source.endswith('.zip'):
                source = source[:-4]
            if target.endswith('.zip'):
                target = target[:-4]

            print(source, target)
            mounts += [docker.types.Mount(type='bind', source= source, target = target)]

            processed_paths += [source, target]

        return mounts, original_paths, processed_paths


    @classmethod
    def process_mount_path(cls, submission, path):
        from main.models import Resource
        # dockerized path transformation
        media_root = os.environ.get('MEDIA_ROOT', None)

        if 'submission.' in path.lower():
            pattern = "submission.([a-zA-Z]*)"
            m = re.match(pattern, path, re.IGNORECASE)
            parameter = m.group(1)
            path = getattr(submission, parameter).path
            if media_root and '/media/' in path:
                return os.path.join(media_root, path.split('/media/')[1])
            else:
                return path
            
        if 'resource.' in path.lower():
            pattern = "resource.([a-zA-Z]*)\[(.*)\]"
            m = re.match(pattern, path, re.IGNORECASE)
            parameter = m.group(1)
            value = m.group(2)

            path = Resource.objects.filter(**{parameter:value})[0].file.path
            if media_root and '/media/' in path:
                return os.path.join(media_root, path.split('/media/')[1])
            else:
                return path
        else:
            if media_root and '/media/' in path:
                return os.path.join(media_root, path.split('/media/')[1])
            else:
                return path
            

    @classmethod
    def process_command_paths(cls, command, original_paths, processed_paths):
        from main.models import Resource
        # dockerized path transformation
        media_root = os.environ.get('MEDIA_ROOT', None)

        for i, path in enumerate(original_paths):
            if path in command:
                command = command.replace(path, processed_paths[i])
        return command