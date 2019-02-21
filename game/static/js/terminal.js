jQuery(function ($, undefined) {
    const BIN_DIR = {
        'bash': '',
        'cat': '',
        'chmod': '',
        'chown': '',
        'cp': '',
        'date': '',
        'df': '',
        'dir': '',
        'echo': '',
        'ed': '',
        'efibootmgr': '',
        'false': '',
        'getfacl': '',
        'grep': '',
        'gzip': '',
        'ip': '',
        'journalctl': '',
        'kill': '',
        'less': '',
        'ln': '',
        'login': '',
        'ls': '',
        'mkdir': '',
        'mktemp': '',
        'more': '',
        'mount': '',
        'mv': '',
        'nano': '',
        'open': '',
        'ping': '',
        'ps': '',
        'pwd': '',
        'readlink': '',
        'rm': '',
        'rmdir': '',
        'sed': '',
        'sh': '',
        'sleep': '',
        'su': '',
        'sync': '',
        'systemctl': '',
        'systemd': '',
        'tar': '',
        'touch': '',
        'true': '',
        'umount': '',
        'urcurious': '',
        'which': '',
    };

    const ROOTFS = {
        'bin': BIN_DIR,
        'boot': {},
        'dev': {},
        'etc': {},
        'home': {
            'sfi': {
                'README': 'The solution must be somewhere here...',
                'passwords': {
                    'dontlook': 'I said don\'t look!'
                }
            },
        },
        'lib': {},
        'lib64': {},
        'lost+found': {},
        'media': {},
        'mnt': {},
        'opt': {},
        'proc': {},
        'root': {},
        'run': {},
        'sbin': {},
        'srv': {},
        'sys': {},
        'tmp': {},
        'usr': {
            'bin': BIN_DIR,
            'include': {},
            'lib': {},
            'local': {},
            'sbin': {},
            'share': {},
            'src': {},
        },
        'var': {
            'cache': {},
            'db': {},
            'empty': {},
            'games': {},
            'lib': {},
            'local': {},
            'lock': {},
            'log': {
                'curl.log': '*   Trying 127.0.0.1...\n' +
                    '* TCP_NODELAY set\n' +
                    '* Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)\n' +
                    '> GET /wowsuchsecret HTTP/1.1\n' +
                    '> Host: localhost:8000\n' +
                    '> User-Agent: curl/7.64.0\n' +
                    '> Accept: */*\n' +
                    '> \n' +
                    '< HTTP/1.1 404 Not Found\n' +
                    '< Date: Thu, 21 Feb 2019 22:45:26 GMT\n' +
                    '< Content-Type: text/html\n' +
                    '< X-Frame-Options: SAMEORIGIN\n' +
                    '< Content-Length: 0\n' +
                    '< \n' +
                    '* Connection #0 to host localhost left intact'
            },
            'mail': {},
            'opt': {},
            'run': {},
            'spool': {},
            'tmp': {},
        },
    };

    const HOME_PATH = '/home/sfi';

    let currentPath = HOME_PATH;

    // Utilities
    function joinPath(...args) {
        let path = args[0];
        if (!path.startsWith('/')) {
            path = '/' + path;
        }

        for (let element of args.slice(1)) {
            if (element === '.' || element === '') {
                // Do nothing
            } else if (element === '..') {
                path = path.replace(/^(.*)(\/.+)$/gm, '$1');
            } else {
                if (path[path.length - 1] !== '/') {
                    path += '/';
                }
                path += element;
            }
        }

        return path === '' ? '/' : path;
    }

    function pathRelativeToAbsolute(path) {
        let newPath = joinPath(...path.split('/'));
        if (!path.startsWith('/')) {
            newPath = joinPath(currentPath, newPath.substr(1));
        }
        return newPath;
    }

    function getFileForPath(path) {
        const elements = path.substr(1).split('/');
        let dir = ROOTFS;

        for (const element of elements) {
            if (element === '') {
                continue;
            }

            if (typeof dir === 'object' && element in dir) {
                dir = dir[element];
            } else {
                return null;
            }
        }

        return dir;
    }

    function fileExists(path) {
        return getFileForPath(path) != null;
    }

    function hasReadAccess(path) {
        return path === '/' ||
            path.startsWith('/home') ||
            path === '/bin' ||
            path === '/usr' ||
            path === '/usr/bin' ||
            path === '/var' ||
            path.startsWith('/var/log');
    }

    function isDirectory(path) {
        return typeof getFileForPath(path) === 'object';
    }

    function isFile(path) {
        return typeof getFileForPath(path) === 'string';
    }

    // Commands
    function execCat(cmd, args) {
        let path = pathRelativeToAbsolute(args[0]);

        if (!fileExists(path)) {
            this.echo('cat: ' + path + ': No such file or directory');
        } else if (!isFile(path)) {
            this.echo('cat: ' + path + ': Is a directory');
        } else if (!hasReadAccess(path)) {
            this.echo('cat: ' + path + ': Permission denied')
        } else {
            this.echo(getFileForPath(path));
        }
    }

    function execEcho(cmd, args) {
        let line = '';
        for (let word of args) {
            line += word + ' ';
        }
        this.echo(line);
    }

    function execCd(cmd, args) {
        let path = args[0];
        if (path === undefined) {
            path = HOME_PATH;
        }
        const newPath = pathRelativeToAbsolute(path);

        if (!fileExists(newPath)) {
            this.echo('cd: no such file or directory: ' + path);
        } else if (!isDirectory(newPath)) {
            this.echo('bash: cd: ' + path + ': Not a directory');
        } else if (!hasReadAccess(newPath)) {
            this.echo('bash: cd: ' + path + ': Permission denied');
        } else {
            currentPath = newPath;
        }
    }

    function execLs(cmd, args) {
        let path = currentPath;
        if (args.length) {
            path = args[0];
        }

        if (!fileExists(path)) {
            this.echo('ls: cannot access \'' + path +
                '\': No such file or directory');
        }
        let dir = getFileForPath(path);
        if (!isDirectory(path)) {
            dir = {[path]: ''}
        }

        let maxLength = 0;
        for (const file in dir) {
            if (dir.hasOwnProperty(file)) {
                maxLength = Math.max(maxLength, file.length);
            }
        }
        maxLength += 2;

        const itemsUntilBreak = Math.floor(this.cols() / maxLength);
        let str = '';
        let i = 0;
        for (const file in dir) {
            if (dir.hasOwnProperty(file)) {
                str += file + ' '.repeat(maxLength - file.length);
            }

            ++i;
            if (i === itemsUntilBreak) {
                this.echo(str);
                str = '';
                i = 0;
            }
        }
        if (str !== '') {
            this.echo(str);
        }
    }

    function execPwd(cmd, args) {
        this.echo(currentPath);
    }

    // Terminal
    const COMMAND_MAP = {
        cat: execCat,
        echo: execEcho,
        cd: execCd,
        ls: execLs,
        pwd: execPwd,
    };

    $('#terminal').terminal(function (command) {
        command = command.trim();
        if (command === '') {
            return;
        }

        command = command.replace(/\s+/g, ' ');
        const words = command.split(' ');
        const cmd = words[0];
        const args = words.slice(1);

        if (cmd in COMMAND_MAP) {
            COMMAND_MAP[cmd].call(this, cmd, args);
        } else {
            this.echo('bash: ' + cmd + ': command not found');
        }
    }, {
        greetings:
            'GNU bash, version 5.0.0(1)-release (x86_64-pc-linux-gnu)\n',
        name: 'bash',
        height: 200,
        prompt: '$ '
    });
});
