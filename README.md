# magic-ghci, remote-control for ghci

magic-ghci runs ghci in a tmux session. It accepts input from the terminal
and via HTTP requests.

Usage:

* Run magic-ghci: `./magic-ghci GHCI_COMMAND GHCI_OPTIONS...`
* Use ghci from the terminal.
* Use HTTP requests to remote control ghci. Examples:
  * Send reload command: `curl --silent --data '' --no-buffer http://localhost:7999/:r`
  * Eval expression `foo 42`: `curl --silent --data '' --no-buffer http://localhost:7999/foo%2042`
* Customize the port magic-ghci listens via the `--port` option. The
  default is 7999.
