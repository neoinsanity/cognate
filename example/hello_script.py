from hello_world import HelloWorld

# Configure with argv string
argv = '--verbose --log_level info --service_name CatWorld --name Cat'
hello_cat = HelloWorld(argv=argv)

# Configure with parameters
hello_dog = HelloWorld(verbose=True,
                       log_level='info',
                       service_name='DogWorld',
                       name='Dog')

hello_cat.run()
hello_dog.run()
