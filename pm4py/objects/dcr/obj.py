from enum import Enum
#from collections import Counter
from typing import Tuple, Generic, TypeVar
#import numpy as np

class Relations(Enum):
    I = 'includesTo'
    E = 'excludesTo'
    R = 'responseTo'
    N = 'noResponseTo'
    C = 'conditionsFor'
    M = 'milestonesFor'


dcr_template = {
    'events': set(),
    'conditionsFor': {},
    'milestonesFor': {},
    'responseTo': {},
    'includesTo': {},
    'excludesTo': {},
    'marking': {'executed': set(),
                'included': set(),
                'pending': set(),
                'executedTime': {},  # Gives the time since a event was executed
                'pendingDeadline': {}  # The deadline until an event must be executed
                },
    'conditionsForDelays': {},
    'responseToDeadlines': {},
    'subprocesses': {},
    'nestings': {},
    'labels': set(),
    'labelMapping': {}
}


class Marking:
    """
    Class object inspired by implementation of prototype of pm4py-dcr
    responsible for storing the state of the DCR graph
    """

    def __init__(self, executed, included, pending) -> None:
        self.__executed = executed
        self.__included = included
        self.__pending = pending

    # getters and setters for datamanipulation, mainly used for DCR semantics
    @property
    def executed(self):
        return self.__executed

    @property
    def included(self):
        return self.__included

    @property
    def pending(self):
        return self.__pending

    # built-in functions for printing a visual string representation
    def __str__(self) -> str:
        return f'( {self.__executed},{self.__included},{self.__pending})'
    def __iter__(self):
        yield 'executed', self.__executed
        yield 'included', self.__included
        yield 'pending', self.__pending

    def __getitem__(self, item):
        classname = self.__class__.__name__
        temp_dict = {}
        for i in self.__dict__.keys():
            if classname not in i:
                newname = i.removeprefix("_" + classname + "__")
                temp_dict[newname] = self.__dict__[i]
        if item in temp_dict:
            return temp_dict[item]
        else:
            return {}


class DCR_Graph(object):
    """
    This implementation is based on the thoery of this Paper:
    Author: Thomas T. Hildebrandt and Raghava Rao Mukkamala,
    Title: Declarative Event-BasedWorkflow as Distributed Dynamic Condition Response Graphs
    publisher: Electronic Proceedings in Theoretical Computer Science. EPTCS, Open Publishing Association, 2010, pp. 59–73. doi: 10.4204/EPTCS.69.5.
    """

    # initiate the objects: contains events ID, activity, the 4 relations, markings, roles and principals
    def __init__(self, template):
        # events and logs are essentially the same, and events was used as an identification for activities
        # in essence, activities were directly mined, but it was based on the event idenfication.
        self.__events = set(template['events'])
        self.__conditionsFor = template['conditionsFor']
        self.__responseTo = template['responseTo']
        self.__includesTo = template['includesTo']
        self.__excludesTo = template['excludesTo']
        self.__marking = Marking(template['marking']['executed'], template['marking']['included'],
                                    template['marking']['pending'])

    # @property functions to extract values used for data manipulation and testing
    @property
    def events(self):
        return self.__events

    @property
    def conditionsFor(self):
        return self.__conditionsFor

    @property
    def responseTo(self):
        return self.__responseTo

    @property
    def includesTo(self):
        return self.__includesTo

    @property
    def excludesTo(self):
        return self.__excludesTo

    @property
    def marking(self):
        return self.__marking


    # in_built functions to print
    def __iter__(self):
        yield 'events', self.__events
        yield 'conditionsFor', self.__conditionsFor
        yield 'milestonesFor', {}
        yield 'responseTo', self.__responseTo
        yield 'includesTo', self.__includesTo
        yield 'excludesTo', self.excludesTo
        yield 'marking', dict(self.__marking)
        yield 'conditionsForDelays', {}
        yield 'responseToDeadlines', {}
        yield 'subprocesses', {}
        yield 'nestings', {}
        yield 'labels', set()
        yield 'labelMapping', {}

    def __repr__(self):
        return str('{' +
                   'events: '+str(self.events) + ', ' +
                   'conditionsFor: '+str(self.conditionsFor) + ', ' +
                   'responseTo: '+str(self.responseTo) + ', ' +
                   'includesTo'+str(self.includesTo) + ', ' +
                   'excludesTo'+str(self.excludesTo) + ', ' +
                   'marking'+str(self.marking)
                   + '}')

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.conditionsFor == other.conditionsFor and self.responseTo == other.responseTo and self.includesTo == other.includesTo and self.excludesTo == other.excludesTo

    def __getitem__(self, item):
        classname = self.__class__.__name__
        #set containing names of superclass if exist
        superClassName = set()
        if self.__class__.__bases__ != {'object'}:
            for base in self.__class__.__bases__:
                superClassName.add(base.__name__)
        temp_dict = {}
        for i in self.__dict__.keys():
            if classname not in i:
                for j in superClassName:
                    newname = i.removeprefix("_" + j + "__")
                    temp_dict[newname] = self.__dict__[i]
            else:
                newname = i.removeprefix("_" + classname + "__")
                temp_dict[newname] = self.__dict__[i]
        if item in temp_dict:
            return temp_dict[item]
        else:
            return {}
"""
class Marking(object):
    """
"""
    This is a per Event marking not a per graph marking
    """
"""
    def __init__(self, executed, included, pending) -> None:
        self.__executed = executed
        self.__included = included
        self.__pending = pending
        self.__last_executed = None
        self.__deadline = None
        super().__init__()

    @property
    def executed(self):
        return self.__executed

    @executed.setter
    def executed(self, value):
        self.__executed = value

    @property
    def included(self):
        return self.__included

    @included.setter
    def included(self, value):
        self.__included = value

    @property
    def pending(self):
        return self.__pending

    @pending.setter
    def pending(self, value):
        self.__pending = value

    @property
    def last_executed(self):
        return self.__last_executed

    @last_executed.setter
    def last_executed(self, value):
        self.__last_executed = value

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, value):
        self.__deadline = value

    def __str__(self) -> str:
        return f'( {self.__executed},{self.__included},{self.__pending})'


class Event(object):

    def __init__(self, n, l, p, g) -> None:
        """
"""
        :param n: name (assumed unique)
        :param l: label
        :param p: parent
        :param g: children (a graph)
        """
"""
        self.__children = g
        self.__loading = False
        self.__parent = p
        self.__name = n
        self.__label = l
        self.__events = set()

        self.__marking = Marking(False, True, False)

        self.__conditions = set()
        self.__responses = set()
        self.__milestones = set()
        self.__includes = set()
        self.__excludes = set()
        super().__init__()

    @property
    def marking(self):
        return self.__marking

    @property
    def conditions(self):
        return self.__conditions

    @property
    def responses(self):
        return self.__responses

    @property
    def milestones(self):
        return self.__milestones

    @property
    def includes(self):
        return self.__includes

    @property
    def excludes(self):
        return self.__excludes

    def isSubProcess(self):
        return len(self.__children.events) > 0

    def enabled(self):
        if isinstance(self.__parent, Event):
            if not self.__parent.enabled():
                return False

        if not self.__marking.included:
            return False

        for e in self.__events:
            if not e.is_accepting():
                return False

        for r in self.__conditions:
            if r.guard:
                e = r.src
                if e.marking.included and not e.marking.executed:
                    return False
                if r.delay:
                    if r.delay > e.marking.last_executed:
                        return False

        for r in self.__milestones:
            if r.guard:
                e = r.src
                if e.marking.included and e.marking.pending:
                    return False

        return True

    def canTimeStep(self, diff):
        if self.__marking.deadline:
            return self.__marking.deadline <= diff

    def timeStep(self, diff):
        if self.__marking.last_executed:
            self.__marking.last_executed = self.__marking.last_executed + diff
        if self.__marking.deadline:
            self.__marking.deadline = self.__marking.deadline - diff

    def execute(self):
        if self.enabled():
            self.__marking.executed = True
            self.__marking.pending = False
            self.__marking.deadline = None
            self.__marking.last_executed = 0

            for r in self.__responses:
                if r.guard:
                    e = r.trg
                    e.marking.pending = True
                    e.marking.deadline = r.deadline

            for r in self.__excludes:
                if r.guard:
                    e = r.trg
                    e.marking.included = False

            for r in self.__includes:
                if r.guard:
                    e = r.trg
                    e.marking.included = True

            if isinstance(self.__parent, Event):
                if self.__parent.enabled():
                    self.__parent.execute()

    def isAccepting(self):
        return not self.__marking.pending and self.__marking.included

    # TODO figure out what to override so that event comparisons work on names and not on labels (I assume labels are
    #  displayed and names are hidden)
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Event):
            return self.__name == o.__name
        elif isinstance(o, str):
            return self.__name == o
        else:
            return super().__eq__(o)

    def __hash__(self) -> int:
        return self.__name.hash()


class DCRGraph(object):

    def __init__(self, pg) -> None:
        self.__parent_graph_temp = pg
        self.__parent = None
        self.__events = set()

    def parent_graph(self):
        if self.__parent is None:
            return self.__parent_graph_temp
        else:
            return self.__parent

    def root(self):
        if self.parent_graph():
            return self.parent_graph().root()
        else:
            return self

    def remove_event(self, o: Event):
        self.__events.remove(o)
        for e in self.__events:
            e.children.remove_event(o)

    def replace_event(self, o: Event, n: Event):
        if o in self.__events:
            for r in o.conditions:
                n.conditions.add(r)
            for r in o.milestones:
                n.milestones.add(r)
            for r in o.responses:
                n.responses.add(r)
            for r in o.includes:
                n.includes.add(r)
            for r in o.excludes:
                n.excludes.add(r)
            self.__events.remove(o)
            for e in self.__events:
                self.replace_in_relation(e.conditions, o, n)
                self.replace_in_relation(e.milestones, o, n)
                self.replace_in_relation(e.responses, o, n)
                self.replace_in_relation(e.includes, o, n)
                self.replace_in_relation(e.excludes, o, n)

    def replace_in_relation(self, r, o, n):
        for e in r:
            if e == o:
                r.remove(o)
                r.add(n)

    def has_event(self, n):
        return self.get_event(n) in self.__events

    def get_event(self, n):
        '''
        Get an event based on name or if it is an Event object with the name in it
        :param n: name of the event (which is unique, unlike the label which can be whatever)
        :return:
        '''
        if n in self.__events:
            if isinstance(n, Event):
                return n
            elif isinstance(n, str):
                for e in self.__events:
                    if e == n:
                        return e
        for e in self.__events:
            if e.children.get_event(n):
                return e.children.get_event(n)
        return None

    def add_loading_event(self, n):
        if self.has_event(n):
            return self.get_event(n)
        elif self.root().has_event(n):
            return self.root().get_event(n)

        e = self.add_event(n)
        e.loading = True
        return e

    def add_event(self, n, l, m, g):
        '''
        :param n: name
        :param l: label
        :param m: marking
        :param g: DCRGraph
        :return:
        '''
        if self.has_event(n) or self.root().has_event(n):
            if self.has_event(n):
                e = self.get_event(n)
            else:
                e = self.root().get_event(n)

            if not e.loading:
                pass  # TODO make an error or exception
            else:
                self.remove_event(e)
                self.root().remove_event(e)
                e.label = l
                e.parent = self
                e.children = g
        else:
            e = Event(n, l, self, g)

        g.parent = e
        e.marking.executed = m.executed
        e.marking.included = m.included
        e.marking.pending = m.pending
        if m.deadline:
            e.marking.deadline = m.deadline
        if m.last_executed:
            e.marking.last_executed = m.last_executed
        self.__events.add(e)

        return e

    def check_src_and_trg_exist(self, src, trg):
        if not self.root().has_event(src):
            eSrc = self.add_loading_event(src)
        else:
            eSrc = self.root().get_event(src)

        if not self.root().has_event(trg):
            eTrg = self.add_loading_event(trg)
        else:
            eTrg = self.root().getEvent(trg)
        return eSrc, eTrg

    def add_condition(self, src, trg, delay, guard=True):
        '''
        src -->* trg
        '''
        eSrc, eTrg = self.check_src_and_trg_exist(src, trg)
        eTrg.conditions.add({'src': eSrc, 'delay': delay, 'guard': guard})

    def add_milestone(self, src, trg, guard=True):
        '''
         src --><> trg
        '''
        eSrc, eTrg = self.check_src_and_trg_exist(src, trg)
        eTrg.milestones.add({'src': eSrc, 'guard': guard})

    def add_response(self, src, trg, deadline, guard=True):
        '''
        src *--> trg
        '''
        eSrc, eTrg = self.check_src_and_trg_exist(src, trg)
        eSrc.responses.add({'trg': eTrg, 'deadline': deadline, 'guard': guard})

    def add_include(self, src, trg, guard=True):
        '''
        src -->+ trg
        '''
        eSrc, eTrg = self.check_src_and_trg_exist(src, trg)
        eSrc.includes.add({'trg': eTrg, 'guard': guard})

    def add_exclude(self, src, trg, guard=True):
        '''
        src -->% trg
        :return:
        '''
        eSrc, eTrg = self.check_src_and_trg_exist(src, trg)
        eSrc.excludes.add({'trg': eTrg, 'guard': guard})

    def execute(self, e):
        if self.has_event(e):
            self.get_event(e).execute()

    def is_accepting(self):
        for e in self.__events:
            if not e.is_accepting():
                return False
        return True

    def can_time_step(self, diff):
        for e in self.__events:
            if not e.can_time_step(diff):
                return False
        return True

    def time_step(self, diff):
        for e in self.__events:
            e.time_step(diff)

    def status(self):
        res = []
        for e in self.__events:
            res.append({'executed': e.marking.executed,
                        'pending': e.marking.pending,
                        'included': e.marking.included,
                        'enabled': e.enabled(),
                        'name': e.name,
                        'lastExecuted': e.marking.last_executed,
                        'deadline': e.marking.deadline,
                        'label': e.label
                        })
            for s in e.children.status():
                s['label'] = f'{e.label}.{s.label}'
                res.append(s)

        return res
"""