#! /usr/bin/python
from jsonschemaplus.validators import Draft4Validator as validator
from jsonschemaplus.errors import ValidationError


SNAPSHOT = 'snapshot'
STATE = 'state'
SYSTEM = 'system'


SUPERVISOR_COMMANDS = ['start', 'stop', 'restart']
SUBSCRIBE_COMMAND = 'sub'
UNSUBSCRIBE_COMMAND = 'unsub'


t = {
    'title': 'Test Schema',
    'type': 'array',
    'properties': {
        'a': {
            'enum': ['a', 'b', 'c', 1]
        },
        'b': {
            'type': 'integer',
            'minimum': 0,
            'maximum': 3
        },
        'c': {
            'minLength': 3
        }
    },
    'required': ['b', 'c'],
    'minimum': 1,
    'maximum': 4,
    'maxLength': 3,
    'maxItems': 2
}


command = {
    'title': 'Supervisor Command',
    'type': 'object',
    'properties': {
        'cmd': {
            'type': 'string',
            'enum': SUPERVISOR_COMMANDS + [SUBSCRIBE_COMMAND] + [UNSUBSCRIBE_COMMAND]  
        },
        'id': {
            'type': 'integer',
            'minimum': 0
        },
        'process': {
            'type': 'string',
            'minLength': 1
        }
    },
    'required': ['cmd', 'id', 'process']
}


snapshot = {
    'title': 'Supervisor Snapshot',
    'type': 'object',
    'properties': {
        SNAPSHOT: {
            'type': 'array',
            'items': [
                {
                    'title': 'Process Snapshot',
                    'type': 'object',
                    'properties': {
                        'group': {
                            'description': 'Process group',
                            'type': 'string',
                            'minLength': 1
                        },
                        'name': {
                            'description': 'Process name',
                            'type': 'string',
                            'minLength': 1
                        },
                        'statename': {
                            'description': 'Process statename',
                            'type': 'string',
                            'enum': ['STOPPED', 'STARTING', 'RUNNING',
                                'BACKOFF', 'STOPPING', 'EXITED', 'FATAL', 'UNKNOWN']
                        },
                        'pid': {
                            'description': 'Application Process Id',
                            'types': ['integer', 'null']
                        },
                        'start': {
                            'description': 'Application Start Time',
                            'type': 'integer',
                            'minimum': 0
                        },
                        'state': {
                            'description': 'Application State Number',
                            'type': 'integer',
                            'enum': [0, 10, 20, 30, 40, 100, 200, 1000]
                        },
                        'stats': {
                            'title': 'Performance metrics array',
                            'type': 'array',
                            'items': [
                                {
                                    'title': 'Metrics snapshot is array of form [timestamp:float, cpu:float, memory:integer]',
                                    'type': 'array',
                                    'minItems': 3,
                                    'maxItems': 3,
                                    'items': [
                                        {
                                            'type': 'number',
                                            'minimum': 0.0
                                        },
                                        {
                                            'type': 'number',
                                            'minimum': 0.0
                                        },
                                        {
                                            'type': 'integer',
                                            'minimum': 0
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    'required': ['group', 'name', 'statename',
                        'pid', 'start', 'state', 'stats']
                }
            ]
        }
    },
    'required': [SNAPSHOT]
}


state = {
    'title': 'Supervisor Application State',
    'type': 'object',
    'properties': {
        STATE: {
            'type': 'object',
            'properties':{
                'group': {
                    'description': 'Application Group',
                    'type': 'string',
                    'minLength': 1
                },
                'name': {
                    'description': 'Application Name',
                    'type': 'string',
                    'minLength': 1
                },
                'statename': {
                    'description': 'Application State Name',
                    'type': 'string',
                    'enum': ['STOPPED', 'STARTING', 'RUNNING',
                        'BACKOFF', 'STOPPING', 'EXITED', 'FATAL', 'UNKNOWN']
                },
                'pid': {
                    'description': 'Application Process Id',
                    'types': ['integer', 'null']
                },
                'start': {
                    'description': 'Application Start Time',
                    'type': 'integer',
                    'minimum': 0
                },
                'state': {
                    'description': 'Application State Number',
                    'type': 'integer',
                    'enum': [0, 10, 20, 30, 40, 100, 200, 1000]
                }
            },
            'required': ['group', 'name', 'statename', 'pid', 'start', 'state']
        }
    },
    'required': [STATE]  
}


system = {
    'title': 'Supervisor System Stats',
    'type': 'object',
    'properties': {
        SYSTEM: {
            'type': 'object',
            'properties': {
                'dist_name': {
                    'description': 'Operating System Distribution Name',
                    'type': 'string',
                    'minLength': 1
                },
                'dist_version': {
                    'description': 'Operating System Version Number',
                    'type': 'string',
                    'minLength': 1
                },
                'hostname': {
                    'description': 'System Hostname',
                    'type': 'string',
                    'minLength': 1
                },
                'processor': {
                    'description': 'Processor Type',
                    'type': 'string',
                    'minLength': 1
                },
                'num_cores': {
                    'description': 'Processor Cores',
                    'type': 'integer',
                    'minimum': 1
                },
                'memory': {
                    'description': 'System Memory',
                    'type': 'integer',
                    'minimum': 0
                }
            },
            'required': ['dist_name', 'dist_version', 'hostname',
                'num_cores', 'memory', 'processor']
        }
    },
    'required': [SYSTEM]
}

z = {
    'minimum': 1,
    'minItems': 3,
    'minLength': 4,
    'items': [{'type': 'integer'}, {'type': 'integer'}]
}

zz = {'enum': [5, 6]}
bb = {'not': {'enum': [1, 2, 3, 4]}}


def main():
    a = validator(t)
    b = validator(command)
    c = validator(snapshot)
    d = validator(state)
    zv = validator(z)

    za = 4
    zb = [1, 2, 3, 4]
    zc = [1, 2]
    zd = 'asdfasdf'
    ze = 'as'
    zf = object()
    zg = 5
    zh = 4
    zi = 3

    for e in zv.errors(za):
        print('error: %s' % e)
            
    for e in zv.errors(zb):
        print('error: %s' % e)

    for e in zv.errors(zc):
        print('error: %s' % e)

    for e in zv.errors(zd):
        print('error: %s' % e)

    for e in zv.errors(ze):
        print('error: %s' % e)

    for e in zv.errors(zf):
        print('error: %s' % e)
    # print('\n\n')
    zzv = validator(zz)
    for e in zzv.errors(za):
        print('error: %s' % e)

    for e in zzv.errors(zd):
        print('error: %s' % e)

    for e in zzv.errors(ze):
        print('error: %s' % e)

    bbb = validator(bb)
    l = list(bbb.errors(zg))
    print(len(l))

    l = list(bbb.errors(zh))
    print(len(l))
    print(l)

    for e in bbb.errors(zg):
        print('error: %s' % e)

    for e in bbb.errors(zh):
        print('error: %s' % e)

    for e in bbb.errors(zi):
        print('error: %s' % e)

    e = validator(system)
    sys = {
        'system': {
            'dist_name': 'Ubuntu_update',
            'dist_version': '15.04_update',
            'hostname': 'agent_1_update',
            'num_cores': 7,
            'memory': 9999999,
            'processor': 'x86_64_update'
        }
    }

    for f in e.errors(sys):
        print('error: %s' % f)

    sys = {
        'system': {
            'dist_name': 'Ubuntu_update',
            'dist_version': '15.04_update',
            'hostname': 'agent_1_update',
            'num_cores': 0,
            'memory': -1000,
            'processor': 'x86_64_update'
        }
    }

    for f in e.errors(sys):
        print('error: %s' % f)


if __name__ == '__main__':
    main()
