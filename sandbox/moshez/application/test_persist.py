
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# System Imports
from twisted.trial import unittest
from twisted.application import persist
from twisted.python import components

class Dummy(components.Componentized):
    pass


objects = [
1,
"hello",
(1, "hello"),
[1, "hello"],
{1:"hello"},
]

class PersistTestCase(unittest.TestCase):
    def testStyles(self):
        for o in objects:
            p = persist.Persistant(o, '')
            for style in 'xml source pickle'.split():
                p.setStyle(style)
                p.save(filename='persisttest.'+style)
                o1 = persist.load('persisttest.'+style, style)
                self.failUnlessEqual(o, o1)

    def testStylesBeingSet(self):
        o = Dummy()
        o.foo = 5
        o.setComponent(persist.IPersistable, persist.Persistant(o, 'lala'))
        for style in 'xml source pickle'.split():
            persist.IPersistable(o).setStyle(style)
            persist.IPersistable(o).save(filename='lala.'+style)
            o1 = persist.load('lala.'+style, style)
            print o1
            self.failUnlessEqual(o.foo, o1.foo)
            self.failUnlessEqual(persist.IPersistable(o1).style, style)


    def testNames(self):
        o = [1,2,3]
        p = persist.Persistant(o, 'object')
        for style in 'xml source pickle'.split():
            p.setStyle(style)
            p.save()
            o1 = persist.load('object.ta'+style[0], style)
            self.failUnlessEqual(o, o1)
            for tag in 'lala lolo'.split():
                p.save(tag)
                o1 = persist.load('object-'+tag+'.ta'+style[0], style)
                self.failUnlessEqual(o, o1)
      
    def testEncryptedStyles(self):
        try:
            import Crypto
        except ImportError:
            raise unittest.SkipTest()
        for o in objects:
            phrase='once I was the king of spain'
            p = persist.Persistant(o, '')
            for style in 'xml source pickle'.split():
                p.setStyle(style)
                p.save(filename='epersisttest.'+style, passphrase=phrase)
                o1 = persist.load('epersisttest.'+style, style, phrase)
                self.failUnlessEqual(o, o1)

    def testPython(self):
        open("persisttest.python", 'w').write('foo=[1,2,3]')
        o = persist.loadValueFromFile('persisttest.python', 'foo')
        self.failUnlessEqual(o, [1,2,3])

    def testEncryptedPython(self):
        try:
            import Crypto
        except ImportError:
            raise unittest.SkipTest()
        phrase='once I was the king of spain'
        open("epersisttest.python", 'w').write(
                          persist._encrypt(phrase, 'foo=[1,2,3]'))
        o = persist.loadValueFromFile('epersisttest.python', 'foo', phrase)
        self.failUnlessEqual(o, [1,2,3])
