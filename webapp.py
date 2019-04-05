import ChangePop


#  We have to disale this i pyllint, because pylint will fail our build every
#  time it encounters this "global" variable

if __name__ == '__main__':
    ChangePop.get_app().run()
