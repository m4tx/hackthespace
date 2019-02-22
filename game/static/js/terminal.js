jQuery(function ($, undefined) {
    const BIN_FILES = [
        'bash', 'cat', 'chmod', 'chown', 'cp', 'date', 'df', 'dir', 'echo',
        'ed', 'efibootmgr', 'false', 'fukulinus', 'getfacl', 'grep', 'ip',
        'kill', 'less', 'ln', 'login', 'ls', 'mkdir', 'mktemp', 'more',
        'mount', 'mv', 'nano', 'open', 'ping', 'ps', 'pwd', 'readlink', 'rm',
        'rmdir', 'sed', 'sh', 'sleep', 'su', 'sync', 'systemctl', 'systemd',
        'tar', 'touch', 'true', 'trythis', 'uname', 'umount', 'urcurious',
        'which'
    ];
    const BIN_DIR = {};
    for (let file of BIN_FILES) {
        BIN_DIR[file] = '';
    }

    const ROOTFS = {
        'bin': BIN_DIR,
        'boot': {},
        'dev': {},
        'etc': {},
        'home': {
            'sfi': {
                'README': 'The solution must be somewhere here...',
                'passwords': {
                    'dontlook': 'I said don\'t look!',
                    'reallydont': 'You are curious, aren\'t you?',
                    'stahp': 'Now let\'s go search somewhere else.',
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

    const LINUS =
        '~~~~~~~~~~~~~~~~~~~~~=====+?77777777?===~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=====+I777?=~~~7777==~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=+???+I7?+++=:...7777=~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~++?I7??777777777?:+7777~~~~~~~~~~~~~~~~~~~~=~~~~~=~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~777I?=7777777777777+?77I7=~~~~~~~~==~~~~~~~===~~===~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~77=:=7777777777777777===?I==~~~~~~~===~~~~~~=~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~7::I7777777777777777777=,77~~~~~~~~~~~~~~~~~~~~~~~=~~~~~==~~\n' +
        '~~~~~~~~~~~~~~~~~~~7+,=7777777777I7I77777777=+7~~~~~~~~~~~~~~~~~~~~~~~~~~====~~~\n' +
        '~~~~~~~~~~~~~~~~~~~7=~?7777I+,:~+I=::,:~+777=+7~~~~~~~~~~~~~~~~~~~~~~~~~~~~~=~~~\n' +
        '~~~~~~~~~~~~~~~~~~~7+~=77I==~::,~7+,,,:=:?77?=7~~~~~~~~=~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~7+~=7?,~:...:~77,:::=?=?7+=7~~~~~~=~====~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~I~~II=I?++=II77I=++?I7777~I~~~~~~~===~~~=~~~~~~=~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~I~,7777??II+7I+I7I7777777=?=~~~~~~=~=~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=7?I7777I+77.,:..+++?I777I:=~~~~~~~~~~~~=~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=:+77I?+=??+~::=?7I+==?77,I=~~~~~~~~~~~~~~=~~~=~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~?=II?=~=I==~~:~~=?+???II77?~~~~~~~~~~~~~~~=~==~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=7=II++++I+?..,=+=,:?????77=~~~~~=~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~77II+++?+=?~:~=III7=+++?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~=+=++I77==???++????+==+I~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '==~~~~~~~~~~~~~~~~~~~===77777+=777~~~=I?+++I7=~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~=++777I?==?777:::===+II7?~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~=++=777I+~++?I77:~~~=+III=7~==~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~+++I++?+=?IIII7~~~==+???:7~::::,.:~====~~~~~~~~~~~~~~~~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~~+=7==~===++IIII~~~====++,77,,,::,...::::~=+++=~~~~~~~=~~~~~\n' +
        '~~~~~~~~~~~~~~~~~~~~==.?==~~~~~~~=~I:~~=====~,77...........,,,,,::::,=~~~~=~~~~~\n' +
        '~~~~~~~~~~~~~~~~..:~~,,?==~~~~~~~~~?+~~~=++~:7I77......,,..........,..~~=~~~~~~~\n' +
        '~~~~~~~~~~====~~:......++==~~=~~~~~I7I7I~:=77I=I7......................~~~~~~~~~\n' +
        '~~~~~~~~~===~~~:::,....I+=~~======~7II777I7II?+=7......................:==~~~~~~\n' +
        '~~~~~~~===~~~::,:::,...7+=~~======77II777I77???+7.......................~~~~~~~~\n' +
        '~~~~~=~::~~,:::,,,,,..~I+========I77?77+7.7II77?7........................=~~~~~~\n' +
        '~~~~:.......,,...,,,,.7?========:.77IIII~=7I7777I........................:=~~~~~\n' +
        '~~~~................,7?+=====++=..+?7777I77777777.........................~==~~~\n' +
        '~==~................=7I+====++=+...77777777777777~.........................~==~=\n' +
        '~=~~.....,,,,,......777~~======7....77777777777777.........................,====\n' +
        '==~=...:...........77777~~~====7....~7777777777777..........................,===\n' +
        '~~~~::,..,.........7777777~~~~=~.....7777777777777...........................:==\n' +
        '~~~~:.:............777777777I77......,777777777777~...........................==\n' +
        '~~~~~~.............777777777777.......I77777777777I............................=\n' +
        '~~~~~~.............~7777777777=........777777777777............................~\n' +
        '~~~~~~:.....,,......~?I7IIII7I.........777777777777~............................\n' +
        '~~~~~~~.....:.........~+?IIII~.........I77I777777777............................\n' +
        '~~~~~~~~..,............~=+++.=.........?I77777777777............................\n' +
        '~~~~~~~~.~..............:++~.?.........I777777777777:...........................\n' +
        '~~~~~~~~=:................~I~I.........I7I7777777777?...........................\n' +
        '~~~~~~~~:..............................I7?77777777777...........................\n' +
        '~~~~~~~~...............................77777777777777...........................\n' +
        '~~~~~~~~..............................=7?777777777777:..........................\n' +
        '~~~~~~~~..............................I77777777777777I..........................\n' +
        '~~~~~~~~:............................,7777777777777777..........................\n' +
        '~~~~~~~~~............................=7777777777777777:.........................\n' +
        '~~~~~~~~=~...........................+7+77777777777777+.........................';

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
    function execBash(cmd, args) {
        this.echo('In order to understand recursion, ' +
            'one must first understand recursion.');
    }

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

    function execEcho(cmd, args) {
        let line = '';
        for (let word of args) {
            line += word + ' ';
        }
        this.echo(line);
    }

    function execFukulinus(cmd, args) {
        this.echo(LINUS);
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

    function execUname(cmd, args) {
        this.echo(
            'Linux sfi-www 2.13.7 x86_64 GNU/Linux. Build 7600. ' +
            'This copy of GNU/Linux is not genuine.');
    }

    // Terminal
    const COMMAND_MAP = {
        bash: execBash,
        cat: execCat,
        cd: execCd,
        echo: execEcho,
        fukulinus: execFukulinus,
        ls: execLs,
        pwd: execPwd,
        uname: execUname,
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
