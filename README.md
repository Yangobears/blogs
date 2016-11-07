# Multi User Blog

This app is an platform that allows multiple user to write posts, get inspired
by others and connect.

## Demo
Go to
```
https://blog-146703.appspot.com/signup
```
to get started. As a user,
you can view posts, create post and delete/edit your own post.
you can also like, comment on others' post.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

```
Python 2.7
Google App Engine
```

## Deployment

In the root directory, run
```
gcloud app deploy app.yaml index.yaml
```
Then
```
gcloud app browse
```
Then go to path '/welcome'

## Built With

* [Webapp2](http://www.dropwizard.io/1.0.2/docs/) - The web framework
* [Google App Engine](https://maven.apache.org/) - Deployment
* [NDB](https://rometools.github.io/rome/) - Database
