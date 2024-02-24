



t0, = axis.plot(xValues, yValues0)
t1, = axis.plot(xValues, yValues1)
t2, = axis.plot(xValues, yValues2)
fig.legend((t0, t1, t2), ('First line', 'Second line', 'Third Line '), 'upper right')



def main():
    print('hello there')
    print('0,0.1401855')
    print('10,0.2336426')
    print('20,0.323877')
    print('30,0.4084717')
    print('40,0.4890381')
    print('50,0.5671875')
    print('60,0.6429199')
    print('70,0.714624')
    print('80,0.7847168')
    print('90,0.8515869')
    print('100,0.9176514')
    print('End')
    print('this is the second line')
    print('this is the line before end')

if __name__ == '__main__':
    main()