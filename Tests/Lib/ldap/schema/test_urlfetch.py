import ldap.schema
from tempfile import NamedTemporaryFile

# Schema from RFC 2247 and related pilot schema
# "Using Domains in LDAP/X.500 Distinguished Names"
# content of file and returned result fomr ldap.schema differs
file_content = "\n".join((
    "dn: cn=schema",
    (
        "attributeTypes: ( 0.9.2342.19200300.100.1.25 NAME "
        "( 'dc' 'domaincomponent' ) DESC 'Standard LDAP attribute type' "
        "EQUALITY caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch "
        "SYNTAX 1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE X-ORIGIN "
        "'RFC 2247' )"
    ),
    (
        "attributeTypes: ( 0.9.2342.19200300.100.1.38 NAME 'associatedName' "
        "DESC 'Standard LDAP attribute type' SYNTAX "
        "1.3.6.1.4.1.1466.115.121.1.12 X-ORIGIN 'RFC 1274' )"
    ),
    (
        "attributeTypes: ( 1.3.6.1.4.1.7165.2.1.37 NAME 'sambaHomePath' "
        "DESC 'Home directory UNC path' EQUALITY caseIgnoreMatch "
        "SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{128} )"
    ),
    (
        "objectClasses: ( 1.3.6.1.4.1.1466.344 NAME 'dcObject' DESC "
        "'Standard LDAP objectclass' SUP top AUXILIARY MUST dc X-ORIGIN "
        "'RFC 2247' )"
    ),
    (
        "objectClasses: ( 0.9.2342.19200300.100.4.14 NAME 'RFC822localPart' "
        "DESC 'Pilot objectclass' SUP domain MAY ( cn $ sn ) X-ORIGIN "
        "'Internet directory pilot' )"
    ),
    (
        "objectClasses: ( 0.9.2342.19200300.100.4.13 NAME 'domain' DESC "
        "'Standard LDAP objectclass' SUP top STRUCTURAL MUST dc MAY "
        "( associatedName $ businessCategory $ description $ "
        "destinationIndicator $ facsimileTelephoneNumber $ "
        "internationalISDNNumber $ l $ o $ physicalDeliveryOfficeName $ "
        "postOfficeBox $ postalAddress $ postalCode $ "
        "preferredDeliveryMethod $ registeredAddress $ searchGuide $ seeAlso "
        "$ st $ street $ telephoneNumber $ teletexTerminalIdentifier "
        "$ telexNumber $ userPassword $ x121Address ) X-ORIGIN 'RFC 2247' )"
    ),
))


schema_dn= "cn=schema"
testcases_schema_attrs = {
    '0.9.2342.19200300.100.1.25': (
        "( 0.9.2342.19200300.100.1.25 NAME ( 'dc' "
        "'domaincomponent' ) DESC 'Standard LDAP attribute type' EQUALITY "
        "caseIgnoreIA5Match SUBSTR caseIgnoreIA5SubstringsMatch SYNTAX "
        "1.3.6.1.4.1.1466.115.121.1.26 SINGLE-VALUE X-ORIGIN 'RFC 2247' )"
    ),
    '0.9.2342.19200300.100.1.38': (
        "( 0.9.2342.19200300.100.1.38 NAME 'associatedName' "
        "DESC 'Standard LDAP attribute type' SYNTAX "
        "1.3.6.1.4.1.1466.115.121.1.12 X-ORIGIN 'RFC 1274' )"
    ),
    '1.3.6.1.4.1.7165.2.1.37': (
        "( 1.3.6.1.4.1.7165.2.1.37 NAME 'sambaHomePath' "
        "DESC 'Home directory UNC path' EQUALITY caseIgnoreMatch "
        "SYNTAX 1.3.6.1.4.1.1466.115.121.1.15{128} )"
    ),
}

testcases_schema_objectclasses = {
    '1.3.6.1.4.1.1466.344': (
        "( 1.3.6.1.4.1.1466.344 NAME 'dcObject' DESC "
        "'Standard LDAP objectclass' SUP top AUXILIARY MUST dc )"
    ),
    '0.9.2342.19200300.100.4.13': (
        "( 0.9.2342.19200300.100.4.13 NAME 'domain' DESC "
        "'Standard LDAP objectclass' SUP top STRUCTURAL MUST dc MAY ( "
        "associatedName $ businessCategory $ description $ "
        "destinationIndicator $ facsimileTelephoneNumber $ "
        "internationalISDNNumber $ l $ o $ physicalDeliveryOfficeName $ "
        "postOfficeBox $ postalAddress $ postalCode $ "
        "preferredDeliveryMethod $ registeredAddress $ "
        "searchGuide $ seeAlso $ st $ street $ telephoneNumber $ "
        "teletexTerminalIdentifier $ telexNumber $ userPassword $ "
        "x121Address ) )"
    ),
    '0.9.2342.19200300.100.4.14': (
        "( 0.9.2342.19200300.100.4.14 NAME 'RFC822localPart' "
        "DESC 'Pilot objectclass' SUP domain STRUCTURAL MAY ( cn $ sn ) )"
    ),
}

with NamedTemporaryFile("w") as f:
    # init testfile
    f.write(file_content)
    f.flush()

    # load from testfile
    url = "file://{}".format(f.name)
    dn, schema = ldap.schema.subentry.urlfetch(url)
    if dn != schema_dn:
        print("DN:")
        print("=>", dn)
        print("differs from", schema_dn)

    # test schema
    for cls, testgroup in (
        (ldap.schema.models.AttributeType, testcases_schema_attrs),
        (ldap.schema.models.ObjectClass, testcases_schema_objectclasses),
    ):
        for oid, expected in testgroup.items():
            entry = str(schema.get_obj(cls, oid))
            if entry != expected:
                print("oid:", oid)
                print("=>", entry)
                print("differs from", expected)
