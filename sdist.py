#!/usr/bin/env python2

import os
import sys
import os.path

from distutils.core import gen_usage
from distutils.debug import DEBUG
from distutils.errors import DistutilsArgError, DistutilsError, CCompilerError
from distutils.util import grok_environment_error

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


def get_distribution(package, command):
    from distutils import core

    save_argv = sys.argv
    core._setup_stop_after = 'init'
    g = {'__file__': os.path.join(PROJECT_PATH, 'setup.py')}
    l = {}

    try:
        sys.argv = ['setup.py', command]
        f = open(os.path.join(PROJECT_PATH, 'setup/%s.py'%(package)))
        try:
            exec f.read() in g, l
        finally:
            f.close()
    except SystemExit:
        pass
    finally:
        sys.argv = save_argv
        core._setup_stop_after = None

    return core._setup_distribution



def replace_sdist_command(dist, package):
    from distutils.command.sdist import sdist as SdistCommandClass

    class NamespacePackageSdistCommandClass(SdistCommandClass):
        def copy_file(self, infile, outfile, preserve_mode=1, preserve_times=1,
                      link=None, level=1):

            if infile == 'setup.py':
                infile = 'setup/%s.py'%(package)
            elif infile == 'MANIFEST.in':
                infile = 'setup/%s.manifest'%(package)

            return SdistCommandClass.copy_file(
                self, infile, outfile, preserve_mode, preserve_times,
                link, level)

    dist.cmdclass['sdist'] = NamespacePackageSdistCommandClass
    cmd_obj = dist.reinitialize_command("sdist")
    cmd_obj.template = 'setup/%s.manifest'%(package)



def main(*packages):
    command = "sdist"

    if packages[0] == 'all':
        packages = [ p[:-3] for p in os.listdir("setup") if p.endswith(".py") ]

    
    for package in packages:
        dist = get_distribution(package, command)
        replace_sdist_command(dist, package)

        try:
            ok = dist.parse_command_line()
        except DistutilsArgError, msg:
            raise SystemExit, gen_usage(dist.script_name) + "\nerror: %s" % msg

        if ok:
            try:
                dist.run_command(command)
            except KeyboardInterrupt:
                raise SystemExit, "interrupted"
            except (IOError, os.error), exc:
                error = grok_environment_error(exc)

                if DEBUG:
                    sys.stderr.write(error + "\n")
                    raise
                else:
                    raise SystemExit, error

            except (DistutilsError,
                    CCompilerError), msg:
                if DEBUG:
                    raise
                else:
                    raise SystemExit, "error: " + str(msg)



if __name__ == '__main__':
    main(*sys.argv[1:])

