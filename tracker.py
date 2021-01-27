# coding: utf-8
# editor: shuhoyo

import json
import argparse
import datetime

# load config
with open('config.json', 'r', encoding='utf-8') as conf:
    config = json.load(conf)

# set external file path
project_file_path = config.get('project_file_path_prefix', './') + 'projects.json'
log_file_path = config.get('log_file_path_prefix', './') + 'record.log'
status_file_path = config.get('status_file_path_prefix', './') + 'STATUS'

with open(project_file_path, 'r', encoding='utf-8') as prj:
    projects = json.load(prj)
    project_nums = list(projects.keys())

dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# `track`
def command_track(args):
    with open(status_file_path, 'r+', encoding='utf-8') as stat:
        project_num = args.p
        memo = args.m
        status = stat.read().strip()
        stat.seek(0)
        if status == 'none':
            task_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            with open(project_file_path, 'r', encoding='utf-8') as prj:
                projects = json.load(prj)
            project_name = projects.get(project_num, 'none')
            stat.write(f'{task_id},{project_name},{dt_now},{memo}')
            stat.truncate()
            print(f'Start job for {project_name}. ({task_id})\n{dt_now}')
        else:
            task_id = status.split(',')[0]
            project_name = status.split(',')[1]
            dt_from = status.split(',')[2]
            memo = status.split(',')[3]
            dt_from_dt = datetime.datetime.strptime(dt_from, '%Y-%m-%d %H:%M:%S')
            dt_now_dt = datetime.datetime.strptime(dt_now, '%Y-%m-%d %H:%M:%S')
            dt_diff = dt_now_dt - dt_from_dt
            stat.write('none')
            stat.truncate()
            with open(log_file_path, 'a', encoding='utf-8') as log:
                log.write(f'{task_id},{project_name},{dt_from_dt},{dt_now_dt},{dt_diff},{memo}\n')
            print(f'Finish job for {project_name}! ({task_id})\n{dt_now}')
            print(f'Elapsed time is {dt_diff}.')

# `status`
def command_status(args):
    with open(status_file_path, 'r', encoding='utf-8') as stat:
        status = stat.read().strip()
        if status == 'none':
            print('No task is in progress.')
        else:
            task_id = status.split(',')[0]
            project_name = status.split(',')[1]
            dt_from = status.split(',')[2]
            print(f'{project_name} is in progress from {dt_from}. ({task_id})')

# `project`
def command_project(args):
    with open(project_file_path, 'r', encoding='utf-8') as prj:
        projects = json.load(prj)
        for k, v in projects.items():
            print(k, v)

# `help`
def command_help(args):
    print(parser.parse_args([args.command, '--help']))

# create parser
parser = argparse.ArgumentParser(description='CLI Time Tracker')
subparsers = parser.add_subparsers()

# `track` command
parser_track = subparsers.add_parser('track', help='see `track -h`')
parser_track.add_argument('-p', choices=project_nums, default='None', help='Project Number (see `project`)')
parser_track.add_argument('-m', default='None', help='Memo')
parser_track.set_defaults(handler=command_track)

# `status` command
parser_status = subparsers.add_parser('status', help='Check current status. (see `status -h`)')
parser_status.set_defaults(handler=command_status)

# `project` command
parser_project = subparsers.add_parser('project', help='Check project list. (see `project -h`)')
parser_project.set_defaults(handler=command_project)

# `help` command
parser_help = subparsers.add_parser('help', help='see `help -h`')
parser_help.add_argument('command', help='Command name which help is shown')
parser_help.set_defaults(handler=command_help)

# parse arguments
args = parser.parse_args()
if hasattr(args, 'handler'):
    args.handler(args)
else:
    # unknown commands
    parser.print_help()





