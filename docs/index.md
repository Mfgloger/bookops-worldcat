# BookOps-Worldcat

[![Build Status](https://travis-ci.com/BookOps-CAT/bookops-worldcat.svg?branch=master)](https://travis-ci.com/BookOps-CAT/bookops-worldcat) [![Coverage Status](https://coveralls.io/repos/github/BookOps-CAT/bookops-worldcat/badge.svg?branch=master&service=github)](https://coveralls.io/github/BookOps-CAT/bookops-worldcat?branch=master) [![PyPI version](https://badge.fury.io/py/bookops-worldcat.svg)](https://badge.fury.io/py/bookops-worldcat) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bookops-worldcat) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

Requires Python 3.7 and up.

Bookops-Worldcat is a Python wrapper around [OCLC's](https://www.oclc.org/en/home.html) [Worldcat](https://www.worldcat.org/) [Search](https://www.oclc.org/developer/develop/web-services/worldcat-search-api.en.html) and [Metadata](https://www.oclc.org/developer/develop/web-services/worldcat-metadata-api.en.html) APIs.  

The Bookops-Worldcat package simplifies some of OCLC API boilerplate, and ideally lowers the technological threshold for cataloging departments that may not have sufficient programming support to access and utilize those web services. Python language, with it's gentle learning curve, has the potential to be a perfect vehicle towards this goal.


This package takes advantage of the functionality of the popular [Requests library](https://requests.readthedocs.io/en/master/). Interaction with OCLC's services is built around Requests sessions. Authorizing a session simply requires  passing in OCLC's WSkey (`SearchSession`) or an access token (`MetadataSession`). Opening a session allows the user to call specific methods which facilitate communication between the user's script/client and a particular endpoint of OCLC's service. Many of the hurdles related to making valid requests are hidden under the hood of this package, making it as simple as possible to access the functionalities of OCLC APIs.  
Please note, not all features of Worldcat Search and Metadata APIs are implemented because this tool was primarily built for our organization's specific needs. However, we are open to any collaboration to expand and improve the package.  


**Supported OCLC web services:**

At the moment, the wrapper supports only OAuth 2.0 endpoints and flows, specifically, it uses Client Credential Grant and Access Token.  


[WorldCat Search API](https://www.oclc.org/developer/develop/web-services.en.html) provides developer-level access to WorldCat for bibliographic, holdings and location data. It requires credentials - WSkey only. It allows searching and retrieving bibliographic records for books, videos, music, and other formats.  
BookOps wrapper offers following operations:  

+ SRU (query in a form of a CQL Search)  
+ Read (retrieves a single bibliographic record by OCLC number)  
+ Lookup By ISBN
+ Lookup By ISSN  
+ Lookup By Standard Number

[Worldcat Metadata API](https://www.oclc.org/developer/develop/web-services/worldcat-metadata-api.en.html) is a read-write service for WorldCat. It allows adding and updating records in WorldCat, mantaining holdings, and working with local bibliographic data. Access to Metadata API requires OCLC credentials. The BookOps wrapper focuses on the following API operations:  

+ Bibliographic Resource  
    + Read (retrieves a single bibliographic record by OCLC number)  
+ Holdings Resource  
    + Set/Create  (to update holdings)
    + Unset/Delete  (to delete holdings)
    + Retrieve Status  (to retrieve holdings status)
    + Batch Set - Multiple OCLC Numbers
    + Batch Unset - Multiple OCLC Numbers


## Installation

To install use pip:  

`$ pip install bookops-worldcat`  


## Quickstart

Worldcat Search API and Metadata API require OCLC credentials which can be obtained at the [OCLC Developer Network](https://www.oclc.org/developer/home.en.html) site. 


#### Searching Worldcat

Search API requires only OCLC WSkey for authorization. Passing the WSkey string to `SearchSession` in the credentials argument will attach it to each request issued while the session is open. `SearchSession` includes several simple lookup methods allowing retrieval of a matching bibliographic record with the highest holdings.

Basic usage:  
```python
>>> from bookops_worldcat import SearchSession

>>> session = SearchSession(credentials="my_WSkey")
>>> result = session.lookup_oclc_number("00000000123")
>>> print(result.status_code)
200
```

Using context manager:  
```python
with SearchSession(credentials="my_WSkey") as session:
    result = session.lookup_isbn(isbn="9781680502404")
    print(result.text)
```
```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<record xmlns="http://www.loc.gov/MARC21/slim">
    <leader>00000cam a2200000 i 4500</leader>
    <controlfield tag="001">1143317889</controlfield>
    ...
    <datafield ind1="1" ind2="0" tag="245">
      <subfield code="a">Blueprint :</subfield>
      <subfield code="b">the evolutionary origins of a good society /</subfield>
      <subfield code="c">Nicholas A. Christakis.</subfield>
    </datafield>
    ...
</record>
```

`SearchSession` allows more complex queries through `sru_query` method:

```python
with SearchSession(credentials="my_WSkey") as session:
  results = session.sru_query(query='srw.au+all+"Asimov Isaac"+and+srw.yr+exact+"1990"')
  print(results.text)
```
```xml
<searchRetrieveResponse xmlns="http://www.loc.gov/zing/srw/" xmlns:oclcterms="http://purl.org/oclc/terms/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:diag="http://www.loc.gov/zing/srw/diagnostic/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<version>1.1</version>
<numberOfRecords>782</numberOfRecords>
<records>
<record>
<recordSchema>marcxml</recordSchema>
<recordPacking>xml</recordPacking>
<recordData>
<record xmlns="http://www.loc.gov/MARC21/slim">
    <leader>00000cam a2200000 a 4500</leader>
    <controlfield tag="001">21153421</controlfield>
    ...
  </record>
</recordData>
</record>
<record>
<recordSchema>marcxml</recordSchema>
<recordPacking>xml</recordPacking>
<recordData>
<record xmlns="http://www.loc.gov/MARC21/slim">
    <leader>00000cam a2200000 a 4500</leader>
    <controlfield tag="001">20561482</controlfield>
    ...
  </record>
</recordData>
</record>
</records>
<nextRecordPosition>11</nextRecordPosition>
<resultSetIdleTime/>
<echoedSearchRetrieveRequest xmlns:srw="http://www.loc.gov/zing/srw/">
<version>1.1</version>
<query>srw.au all "Asimov Isaac" and srw.yr exact "1990"</query>
<maximumRecords>10</maximumRecords>
<recordPacking>xml</recordPacking>
<startRecord>1</startRecord>
<sortKeys>relevance,,0</sortKeys>
<wskey>my_WSkey</wskey>
<frbrGrouping>off</frbrGrouping>
<servicelevel>default</servicelevel>
</echoedSearchRetrieveRequest>
</searchRetrieveResponse>
```

For more details about syntax of queries see the [Advanced Usage>SessionSearch section](https://bookops-cat.github.io/bookops-worldcat/#searchsession-search-api).


#### Obtaining Access Token

Worldcat access token can be obtained by passing credential parameters into `WorldcatAccessToken` object.

```python
from bookops_worldcat import WorldcatAccessToken

token = WorldcatAccessToken(
    oauth_server="https://oauth.oclc.org",
    key="my_WSKey",
    secret="my_secret",
    options={
        "scope": ["WorldCatMetadataAPI"],
        "principal_id": "my_principal_id",
        "principlal_idns": "my_principal_idns"
    },
    agent="my_app/version 1.0"
)
print(token.token_str)
"tk_Yebz4BpEp9dAsghA7KpWx6dYD1OZKWBlHjqW"
```
Note, WorldCat Metadata API requires an access token for authorization.

#### Getting Records

The `MetadataSession` is authorized using `WorldcatAccessToken` object. The session allows retrieving a full bibliographic record from Worldcat by passing its OCLC number in the method's parameter:

Basic usage:
```python
from bookops_worldcat import MetadataSession  

with MetadataSession(credentials=token) as session:
    results = session.get_record("00000000123")
```

or explicit:
```python
results = session.get_record(oclc_number="00000000123")
```

Returned bibliographic record can be acceessed via `text` or `content` (preferable) argument: 

```python
print(results.text)
<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom">
  <content type="application/xml">
    <response xmlns="http://worldcat.org/rb" mimeType="application/vnd.oclc.marc21+xml">
      <record xmlns="http://www.loc.gov/MARC21/slim">
        <leader>00000cam a2200000Ia 4500</leader>
        <controlfield tag="001">ocn850939579</controlfield>
        ...
        <datafield tag="100" ind1="0" ind2=" ">
          <subfield code="a">OCLC RecordBuilder.</subfield>
        </datafield>
        <datafield tag="245" ind1="1" ind2="0">
          <subfield code="a">Record Builder Added This Test Record On 06/26/2013 13:06:22.</subfield>
        ...
        <datafield tag="500" ind1=" " ind2=" ">
          <subfield code="a">TEST RECORD -- DO NOT USE.</subfield>
        </datafield>
        </record>
    </response>
  </content>
  <id>http://worldcat.org/oclc/850939579</id>
  <link href="http://worldcat.org/oclc/850939579"></link>
</entry>
```

#### Updating Holdings

`MetadataSession` can be used to check or set/unset your library holdings on a master record in Worldcat:

example:  
```python
result = session.holdings_set(oclc_number="00000000123")
print(result)
<Response [201]>
```

```python
result = session.holdings_get_status("850939579")
print(result.text)
```
```json
{
 "title":"850939579",
 "content":{"requestedOclcNumber":"850939579","currentOclcNumber":"850939579","institution":"NYP","holdingCurrentlySet":true,"id":"http://worldcat.org/oclc/850939579"},
 "updated":"2020-04-29T05:27:22.960Z"
}
```

For holdings operations on batches of records see [Advanced Usage>MetadataSession>Updating Holdings](https://bookops-cat.github.io/bookops-worldcat/#holdings)

## Advanced Usage

**Identifying your application**

BookOps-Worldcat provides a default `user-agent` value in headers of all requests to OCLC web services: `bookops-worldcat/{version}`. It is encouraged to update the `user-agent` value to properly identify your application to OCLC servers as it may be a useful piece of information for OCLC staff troubleshooting any problems. To set a custom "user-agent" in a session simply update its headers attribute:
```python
session.headers.update({"user-agent": "my-app/version 1.0"})
```

The `user-agent` header can be set for a access token request as well. To do that simply pass it as the `agent` parameter when initiating `WorldcatAccessToken` object:
```python
token = WorldcatAccessToken(
    oauth_server='https://oauth.oclc.org',
    key='WSkey',
    secret='WSsecret',
    options={
        "scope": ['SCOPE1', 'SCOPE2'],
        "principal_id": "PRINCIPAL_ID_HERE",
        "principal_idns": "PRINCIPAL_IDNS_HERE"},
    "agent": "my_app/1.0.0"
)
```

**Event hooks**

`SearchSession` and `MetadataSession` methods support [Requests event hooks](https://requests.readthedocs.io/en/latest/user/advanced/#event-hooks) which can be passed as an argument:  

```python
def print_url(response, *args, **kwargs):
    print(response.url)


hooks = {'response': print_url}

session.get_record("00000000123", hooks=hooks)
```


#### SearchSession (Search API)

WorldCat Search API requires only OCLC's WSKey for authentication ([WSKey Lite pattern](https://www.oclc.org/developer/develop/authentication/wskey-lite.en.html)). Returned records are by default in MARC XML format. Other formats offered by the API are not currently supported.  

##### Simple Lookup
Lookup methods of `SearchSession` always return a single, matching record with highest holdings count in the WorldCat:  

+ `lookup_isbn` performs ISBN search
+ `lookup_issn` performs ISSN search
+ `lookup_oclc_number`  performs OCLC number search
+ `lookup_standard_number` performs standard number query

Fullness of retrieved bibliographic records can be specified by passing a `service_level` argument into each of the requests. There are two modes: "default" and "full".

```python
with SearchSession(credentials="my_WSKey") as session:
    result = session.lookup_isbn("9781680502404", service_level='full')
```

Searches for OCLC numbers that have been merged retrieve a master record they have been merged into:
```python
with SearchSession(credentials="my_WSKey") as session:
    result = session.lookup_oclc_number(oclc_number="969362800")
```
Do not use any "ocm", "ocn", or other prefixes with OCLC numbers.

##### Complex queries

`sru_query` method of `SearchSession` offers a flexible way to build complex queries using SRU/CQL syntax.

Following OCLC's resouces can be very helpful in learning about query syntax:  

+ http://www.worldcat.org/webservices/catalog/search/sru?wskey={my_WSKey}
+ [OCLC Search API documentation](https://www.oclc.org/developer/develop/web-services/worldcat-search-api/bibliographic-resource.en.html)
+ [URI Evaluator](http://worldcat.org/webservices/catalog/evaluator.html)


Advanced CQL query example (keyword search for "civil war" phrase with subject "antietam" or "sharpsburg", results sorted by date from most recent one):  
```python 
with SearchSession(credentials="my_WSKey") as session:
    results = session.sru_query(
        query='srw.kw+=+"civil war"+and+(srw.su+=+"antietam"+OR+srw.su+=+"sharpsburg")',
        maximum_records=50,
        sort_keys=[("date", "descending")],
        service_level="full")
```
Note, `sru_query` does not require to URL encode parenthesis in logic statements as it is in the OCLC documentation.


Default parameters of the `sru_query` method:  

+ `start_record` (default value: `1`): starting position of the result set (can be used to page through the large results)  
+ `maximum_records` ( default: `10`):  maximum value is 100
+ `sort_keys` (default: `[("relevance", "descending")]`): specifies how results are sorted; `sort_keys` must be a list of tuples, where the first tuple element is a key, and the second is a sort type. This allows to combine two or more sort types in the results, for example: `sort_keys=[("author", "ascending"), ("date", "descending")]` will return results sorted by the author in alphabetical order and within each author group results will be sorted by date from the newest to oldest; sort_keys keys:  
    + relevance
    + title
    + author
    + date
    + library_count
    + score
+ `frbr_grouping` (default: `"off"`): options `"on"` and `"off"` turn on or off FRBR grouping
+ `service_level` (default: `"default"`):  options: `"default"` or `"full"`
+ `hooks` (default: `None`): optional event hooks



#### WorldcatAccessToken

Bookops-Worldcat utilizes OAuth 2.0 and Client Credential Grant flow to aquire Access Token. Please note, your OCLC credentials must allow access to Metadata API in their scope to be permitted to make requests to the web service.

Obtaining:
```python
from bookops_worldcat import WorldcatAccessToken
token = WorldcatAccessToken(
    oauth_server="https://oauth.oclc.org",
    key="my_WSKey",
    secret="my_secret",
    options={
        "scope": ["WorldCatMetadataAPI"],
        "principal_id": "my_principal_id",
        "principlal_idns": "my_principal_idns"
    },
    agent="my_app/version 1.0"
)
```

Token object retains underlying Requests object functionality (`requests.Request`) that can be accessed via `.server_response` attribute:

```python
print(token.server_response.status_code)
200
print(token.server_response.elapsed):
0:00:00.650108
print(token.server_response.json())
```
```json
{
"user-agent": "bookops-worldcat/0.1.0",
"Accept-Encoding": "gzip, deflate",
"Accept": "application/json",
"Connection": "keep-alive",
"Content-Length": "67",
"Content-Type": "application/x-www-form-urlencoded",
"Authorization": "Basic encoded_authorization_here="
}
```

Checking if token is expired can be done by calling `is_expired` method on it:
```python
print(token.is_expired())
True
```

A failed token request raises `TokenRequestError` which provides returned by the server error code and detailed message.

#### MetadataSession

A wrapper around WorldCat Metadata API. MetadataSession inherits `requests.Session` methods.  
Returned bibliographic records are by default in MARC/XML format (OCLC's native CDF XML and the CDF translation into JSON serializations are not supported at the moment).

##### get_record Method

`session.get_record()` method with OCLC number as an argument sends a request for a matching full bibliographic record in Worldcat. `get_record` should be a primary method to download records from Worldcat. The Metadata API correctly matches requested OCLC numbers of records that have been merged by returning current master record.

Returned response is a `requests.Response` object with all its features:
```python
with MetadataSession(credentials=token) as session:
    result = session.get_record("00000000123")
    print(result.status_code)
    print(result.url)
200
"https://worldcat.org/bib/data/00000000123"
```
To avoid any `UnicodeEncodeError` it is recommended to access retrieved data with `.content` attribute of the response object:
```python
print(response.content)
```

##### Holdings

MetadataSession supports fallowing holdings operations:  

+ `holdings_get_status` retrieves holding status of requested record 
+ `holdings_set` sets holdings on an individual bibliographic record
+ `holdings_unset` deletes holdings on an individual bibliographic record
+ `holdings_set_batch` allows to set holdings on multiple records; it is not limited by OCLC 50 bibs limit)
+ `holdings_unset_batch` allows to delete holdings on multiple records and is not limited to OCLC's 50 records restriction

By default, responses are returned in `atom+json` format, but `atom+xml` can be specified:
```python
result = session.holdings_get_status("1143317889", response_format="xml")
print(result.text)
```
```xml
<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom">
  <title type="text">1143317889</title>
  <updated>2020-04-25T05:21:10.233Z</updated>
  <content type="application/xml">
    <holdings xmlns="http://worldcat.org/metadata-api-service">
      <requestedOclcNumber>1143317889</requestedOclcNumber>
      <currentOclcNumber>1143317889</currentOclcNumber>
      <institution>NYP</institution>
      <holdingCurrentlySet>true</holdingCurrentlySet>
      <id>http://worldcat.org/oclc/1143317889</id>
    </holdings>
  </content>
</entry>
```

Pass OCLC record numbers for batch operations as a list of strings:  
```python
session.holdings_unset_batch(
    oclc_numbers=[
        "00000000123",
        "00000000124",
        "00000000125",
        "00000000126"
    ]
)
```
The web service limits number of records in a batch operation to 50, but `MeatadataSession` permits larger batches by spliting them into chunks of 50 and issuing automaticaly multiple requests. The return object is a list of returned from server results.