# Architecture

Here is a general overview of the architecture. It is based only on managed AWS services
in order to reduce the production overhead.

Details are given after the schema.

```
   +---------+          +---------+                      +----------------------------------+
   |         |          |         |                      |                                  |
   |         |          |         |                      | DynamoDB                         |
   | Website |          | Storage |                      | Table                            |
   | Bucket  |     +----> Bucket  <--------------+   +--->                                  <------+
   |         |     |    |         |              |   |   | Storage for exchanges and tokens |      |
   |         |     |    |         |              |   |   |                                  |      |
   +----^----+     |    +---------+              |   |   +----------------------------------+      |
        |          |                             |   |                                             |
        |          |                             |   |                                             |
        |          |                S3 presigned |   | Exchanges and token management              | Validity of tokens checking
        |          |                up/down load |   |                                             |
        |          |                url creation |   |                                             |                                 Authentication based
        |          |                             |   |                                             |                                 on Google through Cognito
        |          |                             |   |                                             |
        |          |                         +---+---+--------------+          +-------------------+-------+     +---------+      +-------------------+
        |          |                         |                      |          |                           |     |         |      |                   |
        |          |                         | λ Code               |          | λ Authorizer              |     | Cognito |      | Google            |
        |          |                         | Exchanges management |          |                           |     |         +------> Identity provider |
        |          |                         |                      |          |                           |     |         |      |                   |
        |          |                         +------^---------------+          +-------------^-------------+     +-----^---+      +-------------------+
        |          |                                |                                        |                         |
        |          | File retrieval                 |                                        |                         |
        |          | with presigned          +------+------+                                 |                         |
        |          | url                     |             |                                 |                         |
        |          |                         | API Gateway +---------------------------------+-------------------------+
        |          |                         | Endpoints   |
        |          |                         |             |             Authentication Delegation
        |          |                         +------^------+
        |          |                                |
        |          |                                |
        |          |      +-------------+           |
        |          |      |             |           |
        |          |      |  User       |           |
        +----------+------+  Browser    +-----------+
                          |             |
                          +-------------+
                                 X
                               XXXXX
```

## General guidelines

The architecture is based on the concept of _exchange_: an exchange represents the exchange of a file 
between someone _inside_ the organization with someone _outside_ the organization, regardless
of the orientation. It can be someone sending a file to a client _outside_ the organization as well
as someone receiving a file _inside_ the organization from the outside.

Each _exchange_ contains the identity of the person of the organization who created it, and a couple of upload
and download tokens.

### Storage

#### Exchange storage

Exchanges are stored in a dynamodb table, with a uuid as index. This table is accessed by:
- The code for executing CRUD operations en exchanges
- The lambda authorizers which are used to validate token for upload/download operations

#### File storage

Files are stored in a private S3 bucket after their upload. In order for users to be able to upload
or download files, presigned S3 urls are generated for a short lifespan when they need to execute this operation.
You can learn more about [S3 presigned urls here.](https://docs.aws.amazon.com/AmazonS3/latest/dev/PresignedUrlUploadObject.html)

Note that files have a limited lifetime due to a scheduled cleaning

#### Website storage

The UI is exposed as a React SPA with S3 bucket website capability.

### Code

The backend code is split in two functional parts:
- One for managing exchanges. It is behind the CRUD API endpoints for exchanges
- One for validating up/down load tokens. It is presented as a lambda authorizer

### Authentication

Authentication is required for using this service. We have two different populations to consider:
- Users inside the organization, who must be able to create exchanges and upload / download files for the exchanges
that they created
- Users outside the organization, who must be able to upload / download files only for the exchanges for which 
they have a token

This leads to a separate authentication.

#### Exchanges management

Exchanges management is protected by a Cognito authentication, which is itself based on a Google authentication. This 
authentication protects the CRUD for exchanges so only people inside the organization and authenticated with Google may
manage exchanges

#### File upload / download

File upload and download is protected by a custom `lambda authorizer`. You can learn more about 
[lambda authorizers here.](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html)

The lambda authorizers check that the upload or download token associated with a file upload or download request is
valid.