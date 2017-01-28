#!/usr/bin/env python

#
# Generated Sat Jan 28 16:37:08 2017 by generateDS.py version 2.24a.
#
# Command line options:
#   ('--super', 'unbsun')
#   ('-o', 'unbsun.py')
#   ('-s', 'unbsunsubs.py')
#
# Command line arguments:
#   local_data/xml/TestbedSunJun13Flows.xsd
#
# Command line:
#   /home/karan/Development/src/github.com/karanthukral/FYDP/venv/bin/generateDS --super="unbsun" -o "unbsun.py" -s "unbsunsubs.py" local_data/xml/TestbedSunJun13Flows.xsd
#
# Current working directory (os.getcwd()):
#   FYDP
#

import sys
from lxml import etree as etree_

import unbsun as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'utf-8'

#
# Data representation classes
#


class datarootSub(supermod.dataroot):
    def __init__(self, generated=None, TestbedSunJun13Flows=None):
        super(datarootSub, self).__init__(generated, TestbedSunJun13Flows, )
supermod.dataroot.subclass = datarootSub
# end class datarootSub


class TestbedSunJun13FlowsSub(supermod.TestbedSunJun13Flows):
    def __init__(self, appName=None, totalSourceBytes=None, totalDestinationBytes=None, totalDestinationPackets=None, totalSourcePackets=None, sourcePayloadAsBase64=None, sourcePayloadAsUTF=None, destinationPayloadAsBase64=None, destinationPayloadAsUTF=None, direction=None, sourceTCPFlagsDescription=None, destinationTCPFlagsDescription=None, source=None, protocolName=None, sourcePort=None, destination=None, destinationPort=None, startDateTime=None, stopDateTime=None, Tag=None):
        super(TestbedSunJun13FlowsSub, self).__init__(appName, totalSourceBytes, totalDestinationBytes, totalDestinationPackets, totalSourcePackets, sourcePayloadAsBase64, sourcePayloadAsUTF, destinationPayloadAsBase64, destinationPayloadAsUTF, direction, sourceTCPFlagsDescription, destinationTCPFlagsDescription, source, protocolName, sourcePort, destination, destinationPort, startDateTime, stopDateTime, Tag, )
supermod.TestbedSunJun13Flows.subclass = TestbedSunJun13FlowsSub
# end class TestbedSunJun13FlowsSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'dataroot'
        rootClass = supermod.dataroot
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'dataroot'
        rootClass = supermod.dataroot
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'dataroot'
        rootClass = supermod.dataroot
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'dataroot'
        rootClass = supermod.dataroot
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from unbsun import *\n\n')
        sys.stdout.write('import unbsun as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
