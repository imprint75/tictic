# tictic
It's a tic-tac-toe playing program created with
Python 3, Django, uWsgi, Nginx and Redis 

Installation (OSX and Linux)
======
If you have [Git](https://git-scm.com/downloads), [VirtualBox](https://www.virtualbox.org/), [Vagrant](https://www.vagrantup.com/) and [Fabric](https://www.fabfile.org/) 
installed locally and you'd like to create a virtual machine to run tictic on, you following these steps:

1. Clone this repo to the directory of your choosing `git clone git@github.com:imprint75/tictic.git` 

2. cd into the repo `cd tictic`

3. Run `vagrant up`
  - this Vagrantfile looks for an Ubuntu box called "ubuntu/trusty64".  If you don't happen to have one of these locally, this step could take a while depending on your connection

4. Run `fab vagrant build`
  - this step can take a little while and requires you to answer y/n to a series of questions.  The answer to all the questions is y.

If you want to install this program to your own server, you probably know how to do this.  Some notes on that:
  - to make setup steps extra clear, I made the whole install fabric based.  The steps required to set it up 
  are basically just following the function called `build` in fabfile.py.  Omit everything that's not required for your system and be mindful
  of the fact that `build` overwrites nginx's default configuration in order to avoid instructions involving hosts modifications

Game Play
======
Assuming you followed the Virtualbox instructions, you should be able to start a new game by making a GET request to `192.168.33.103/start`.  You can do this opening a terminal and typing

`curl 192.168.33.103/start`

This should return something along the lines of

`{"gid": "7896ca16-7252-4280-9117-76569a760c49", "board": [[null, null, null], [null, null, null], [null, null, null]]}`

In this json, `gid` is your game id.  This must be included in every request you make to the program while playing and it will be returned in every response form the server.
The board paramter represents a 3X3 tic-tac-toe board as a list containing 3 lists with 3 items each.  You can envision the 
spaces on the board as

| 0 | 1 | 2 |
| --- | --- | --- |
| **3** | **4** | **5** |
| **6** | **7** | **8** |

The url to make a move requires you to make a POST request to `192.168.33.103/move` and include the parameters `gid` and `move`.  If you wanted to grab the middle square on the board, for example, you could run this command

`curl --data "gid=7896ca16-7252-4280-9117-76569a760c49&move=4" 192.168.33.103/move`

The response might look like this

`{"gid": "7896ca16-7252-4280-9117-76569a760c49", "board": [[null, null, null], [null, "X", null], [null, null, "O"]]}`

Assuming you didn't encounter an error or a winning move, the program just responds with the `gid` and the full `board`.  You can see from this response that the program selected space 8, so you can't select 8 on your next move.  You may encounter `error` and `winner` messages as encountered.
