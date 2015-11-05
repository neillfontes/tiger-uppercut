import ConfigParser
import StringIO
import os


class PropertyReader:

    @staticmethod
    def read_properties_file(file_path):
        with open(file_path) as f:
            config = StringIO.StringIO()
            config.write('[dummy_section]\n')
            config.write(f.read())
            config.seek(0, os.SEEK_SET)

            cp = ConfigParser.SafeConfigParser()
            cp.readfp(config)

            return dict(cp.items('dummy_section'))
