# cli_timetrack
Timetracker on command line interface written in Python.

## Usage
### Preparation
1. Clone this repository. `git clone https://github.com/shuhoy/cli_timetracker.git`
2. Edit `projects.json` and `config.json`.
3. Create alias  of `python tracker.py`. (optional)

### Command
#### project
Display project number and project name.

`python tracker.py project`

#### track
Start/Stop tracking.

`python tracker.py track -p <PROJECT_NUMBER> -m <MEMO>`

#### status
Display current tracking status.

`python tracker.py status`

## Object
- config.json
  - Configuration of path to the log file and loaded file.
- projects.json
  - Correspondence of project-name and project-number.

## ToDo
- Add exception handling.

