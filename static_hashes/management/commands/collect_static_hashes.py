import json
import os
import subprocess
import time

from django.conf import settings
from django.core.management.base import NoArgsCommand

from static_hashes import utils


class Command(NoArgsCommand):
    hashes = {}
    get_hash_command = "git blame {path} | sort -b -k 3 -r | head -1 | awk '{{print $1}}'"
    get_current_hash = "git rev-parse --short HEAD"
    def handle(self, **options):
        self.walk_static_dirs()
        self.write_output_files()
        self.output_end_command_data()

    def walk_static_dirs(self):
        self.hashed_files_number = 0
        self.command_start_time = time.time()

        for staticfile_dir in utils.STATIC_DIRS:
            staticfile_dir = staticfile_dir['dir']
            os.chdir(staticfile_dir)
            for root, dirs, files in os.walk(staticfile_dir):
                for file in files:
                    print "#############"
                    print "root:" + root
                    print "file: " + file
                    print "dirs: "
                    print dirs
                    print "#############"
                    try:
                        path = os.path.join(root, file)
                        if os.path.isfile(path) and path.lower().endswith(('.js', '.css', '.html', '.htm')):
                            self.add_hash(path)
                            self.increment_file_number()
                            print path
                    except IOError, e:
                        if e.errno == errno.EPIPE:
                            pass
                        else:
                            print e

    def add_hash(self, path):
        self.hashes[self.transform_path(path)] = self.get_commit_hash(path)

    def get_commit_hash(self, path):
        command = self.get_hash_command.format(path=path)
        commit_hash = subprocess.check_output(command, shell=True)
        return self.transform_commit_hash(commit_hash)

    @staticmethod
    def transform_commit_hash(commit_hash):
        return commit_hash.strip()

    @staticmethod
    def transform_path(path):
        """Convert local path to path browser will be requesting."""
        return utils.local_to_browser_path(path)

    def serialize(self):
        self.hashes['__current__'] = self.transform_commit_hash(
            subprocess.check_output(self.get_current_hash, shell=True)
        )
        return json.dumps(self.hashes)

    def navigate_to_output_dir(self):
        if not os.path.exists(settings.STATIC_HASHES_OUTPUT_DIR):
            os.makedirs(settings.STATIC_HASHES_OUTPUT_DIR)
        os.chdir(settings.STATIC_HASHES_OUTPUT_DIR)

    def write_output_files(self):
        self.navigate_to_output_dir()
        self.write_js_output_file()
        self.write_json_output_file()

    def write_js_output_file(self):
        with open(os.path.join(settings.STATIC_HASHES_OUTPUT_DIR, 'static-hashes.js'), 'w') as f:
            f.write('var hashes = ' + self.serialize())

    def write_json_output_file(self):
        with open(os.path.join(settings.STATIC_HASHES_OUTPUT_DIR, 'static-hashes.json'), 'w') as f:
            f.write(self.serialize())

    def increment_file_number(self):
        self.hashed_files_number = self.hashed_files_number + 1

    def output_end_command_data(self):
        print '\nGrabbed hash for %s files in %s seconds.' % (self.hashed_files_number, time.time() - self.command_start_time)
 