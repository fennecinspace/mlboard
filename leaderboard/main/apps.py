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
                    # submission.status = 'PROCESSING'
                    submission.save()
                    cls.run_container(submission)
                    submission.status = 'DONE'
                    submission.save()
                except Exception as e:
                    # submission.status = 'ERROR'
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
        mounts = cls.create_mounts(submission)

        print('Launching Container')
        results = client.containers.run(
            image, 
            command,
            mounts = mounts,
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

        args = submission.challenge.processor.command.split(' ')
        for i in range(len(args)):
            if args[i].strip() != '-v':
                continue

            source, target = args[i+1].split(':')

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

        return mounts


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