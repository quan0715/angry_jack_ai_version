# angry_jack_ai_version
### How to use
Run `python main.py`.
There are some options you can use:
- `-t` or `--train`, if you set this option, the program will train a snake model.
- `-v` or `--test`, test the snake model. Requires a file as argument.
- `-l` or `--save_log`, set this option if you need to save the log of the training process.
- `-d` or `--display`, opens the pygame client, and you can see the visualization.

### Example
`python main.py -t -l -d` begin training, the program will display the process by launching pygame. The log is also saved as `{datetime}.txt`.

`python main.py -v /path/to/snake_model` tests the snake model and prints the final score.
If you want to see the visualization, just add `-d` option.
