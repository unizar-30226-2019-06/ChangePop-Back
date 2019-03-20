import ChangePop


#  We have to disale this i pyllint, because pylint will fail our build every
#  time it encounters this "global" variable
app = ChangePop.create_app() # pylint: disable=invalid-name


if __name__ == '__main__':
    app.run()
