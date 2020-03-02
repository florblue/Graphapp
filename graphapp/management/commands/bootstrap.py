# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.core.management.base import BaseCommand
from django.db import DatabaseError
import uuid
from graphapp.models import Person
from graphapp import db

__author__ = 'lundberg'


class Command(BaseCommand):
    help = 'Create a NodeHandle and set handle_id for nodes missing handle_id property'

    def handle(self, *args, **options):
        with db.manager.session as s:
            s.run('CREATE CONSTRAINT ON (p:Person) ASSERT p.handle_id IS UNIQUE')
            
            try:
                q = """
                    OPTIONAL MATCH (p:Person) WHERE NOT exists(p.handle_id) WITH collect(id(p)) as persons
                    RETURN persons
                    """

                record = s.run(q).single()
                
                persons = record['persons']
            except IndexError:
                persons = [], []

        q = 'MATCH (n) WHERE ID(n) = $node_id SET n.handle_id = $handle_id'
        p = 0
        
        person_objs = []

        with db.manager.transaction as t:
            try:
                for node_id in persons:
                    person = Person(handle_id=str(uuid.uuid4()))
                    person_objs.append(person)
                    t.run(q, {'node_id': node_id, 'handle_id': person.handle_id})
                    p += 1
            except Exception as e:
                raise e
            else:
                try:
                    Person.objects.bulk_create(person_objs)
                except DatabaseError as e:
                    raise e

        self.stdout.write('Successfully completed! Added %d persons.' % (p))
