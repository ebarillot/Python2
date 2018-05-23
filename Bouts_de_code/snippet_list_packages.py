# coding=utf-8

from __future__ import print_function, unicode_literals

import cassandra
import pkgutil

package=cassandra

# for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
#     print("Found submodule %s (is a package: %s)" % (modname, ispkg))


prefix = package.__name__ + "."
for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
    print("Found submodule %s (is a package: %s)" % (modname, ispkg))
    # module = __import__(modname, fromlist=[b"dummy"])
    # print("Imported", module)

