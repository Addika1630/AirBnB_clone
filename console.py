#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Console Module
    This module controls all databases.
    Can create, modify and delete instances.
"""


from datetime import datetime
import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re
import shlex


class HBNBCommand(cmd.Cmd):
    """command processor class."""
    prompt = '(hbnb) '
    allowed_classes = ['BaseModel', 'User', 'State', 'City',
                       'Amenity', 'Place', 'Review']

    def do_quit(self, line):
        """Quit command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """Quit command to exit the program.
        """
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel.
        """
        command = self.parseline(line)[0]
        if command is None:
            print('** class name missing **')
        elif command not in self.allowed_classes:
            print("** class doesn't exist **")
        else:
            new_obj = eval(command)()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance
based on the class name and id.
        """
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]
        if command is None:
            print('** class name missing **')
        elif command not in self.allowed_classes:
            print("** class doesn't exist **")
        elif arg == '':
            print('** instance id missing **')
        else:
            inst_data = models.storage.all().get(command + '.' + arg)
            if inst_data is None:
                print('** no instance found **')
            else:
                print(inst_data)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        command = self.parseline(line)[0]
        arg = self.parseline(line)[1]
        if command is None:
            print('** class name missing **')
        elif command not in self.allowed_classes:
            print("** class doesn't exist **")
        elif arg == '':
            print('** instance id missing **')
        else:
            key = command + '.' + arg
            inst_data = models.storage.all().get(key)
            if inst_data is None:
                print('** no instance found **')
            else:
                del models.storage.all()[key]
                models.storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances
based or not on the class name.
        """
        command = self.parseline(line)[0]
        objs = models.storage.all()
        if command is None:
            print([str(objs[obj]) for obj in objs])
        elif command in self.allowed_classes:
            keys = objs.keys()
            print([str(objs[key]) for key in keys if key.startswith(command)])
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and id
by adding or updating attribute.
        """
        args = shlex.split(line)
        args_size = len(args)
        if args_size == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        elif args_size == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            inst_data = models.storage.all().get(key)
            if inst_data is None:
                print('** no instance found **')
            elif args_size == 2:
                print('** attribute name missing **')
            elif args_size == 3:
                print('** value missing **')
            else:
                args[3] = self.analyze_parameter_value(args[3])
                setattr(inst_data, args[2], args[3])
                setattr(inst_data, 'updated_at', datetime.now())
                models.storage.save()

    def analyze_parameter_value(self, value):
        """Checks a parameter value for an update

        Analyze if a parameter is a string that needs
        convert to a float number or an integer number.

        Args:
            value: The value to analyze

        """
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)

        return value

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        obj = models.storage.all()
        class_name = arg.split('.')[0] if '.' in arg else arg
        c = [obj for obj in obj.values() if type(obj).__name__ == class_name]
        print(len(c))

    def precmd(self, line):
        """ Preprocesses a line of input before executing a command.

        Args:
            line (str): The input line to be processed.

        Returns:
            str: The processed input line.

        Raises:
            None
        """

        args = line.split('.')
        if len(args) >= 2:
            if args[1].count('()') == 1:
                class_name = args[0]
                a = args[1].replace('(', '.')
                b = a.replace(')', '.')
                c = b.split('.')
                command = c[0]
                line = f"{command} {class_name}"
            elif args[1].count('(') == 1 and args[1].count(')') == 1:
                class_name = args[0]
                a = args[1].replace('(', '.')
                b = a.replace(')', '.')
                c = b.split('.')
                command = c[0]
                arguments = c[1].replace('{', '').replace('}', '')
                arguments = arguments.replace(':', ' ').replace(',', '')
                arguments = arguments.replace('"', '')
                arguments = arguments.replace("'", '')
                line = f"{command} {class_name} {arguments}"

        return line

    def emptyline(self):
        """Empty line"""

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
