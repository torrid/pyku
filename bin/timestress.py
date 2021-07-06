import time


def stress(seconds):
    assert type(seconds) == type(1) and seconds < 120
    start=time.time()
    while True:
        a=1
        while a < 1000:
            x=a*a
            x=1.3333*x/(a+3.333)
            a+=1

        e=time.time()-start
        if e > seconds:
            break

stress(10)

