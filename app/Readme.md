# Application Files

## Working with the Container Image

Our application will be containerized, and the configuration for the base image can be found the Dockerfile in this directory. 

Development can take place locally, and in order to do this as well as test, build and run containers locally, you will need [Docker Desktop](https://docs.docker.com/desktop/).

### Helpful Docker Commands

- #### Create an image from the Dockerfile:

```console

#This command must be run from the same directory as the Dockerfile

docker build -t 

```

- #### Check for available images locally:

```console

docker images  

```

- #### Run a container locally in interactive mode:

```console

docker run -it image_name:tag sh   

```