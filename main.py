import calculator
from bokeh.plotting import figure, output_file, save,show



def test(count):
    calcul = calculator.calculator(24)
    counter=0
    for i in range(count):
        if(calcul.calculate_all()>calcul.calculate_all(False)):
            counter+=1
    return counter/count

def calculate_average_on_n_with_and_without_active_failover(n,stat=False,model_type='default'):
    if(model_type=='default'):
        calcul=calculator.calculator(24)
    else:
        calcul=calculator.calculator(25,'mod')
    average=[]
    sum=0
    print("Calculating average reliability value on",n)
    for i in range(n):
        sum+=calcul.calculate_all()
        #print("iteration with active failover",i)
    average.append(sum/n)
    sum=0
    calcul.print_statistics()
    calcul.null_statistic()
    for i in range(n):
        sum += calcul.calculate_all(False)
        #print("iteration without failover",i)
    average.append(sum/n)
    if(stat):
        calcul.print_statistics()
    return average

if(__name__=="__main__"):
    #calcul=calculator.calculator(25,'mod')
    calcul = calculator.calculator(24)
    #print("Testing")
    #print(test(100))
    #print(calcul.calculate_all())
    #calcul.print_statistics()
    #print(calcul.calculate_all(False))
    avg=calculate_average_on_n_with_and_without_active_failover(10,True)
    print("(Statistic for active failover)")
    print("With active failover ",avg[0])
    print("Without active failover ", avg[1])
    #average on 100 result about 0.9903089689876827 with failover
    #without - 0.9890357463003508
    print("Modified:")
    avg_mod=calculate_average_on_n_with_and_without_active_failover(10,True,'mod')
    print("(Statistic for active failover)")
    print("With active failover ",avg_mod[0])
    print("Without active failover ", avg_mod[1])

    pointsY_with_active_failover=calcul.calculate_points(True)
    # cumulative=pointsY_with_active_failover.copy()
    # cumulative[0]+=cumulative[1]+cumulative[2]+cumulative[3]
    # cumulative[1]+=cumulative[2]+cumulative[3]
    # cumulative[3]+=cumulative[4]
    # print(cumulative);
    #
    # print(pointsY_with_active_failover)
    # pointsX=[0,1,2,3,4]
    # pointsY_without_active_failover = calcul.calculate_points(False)
    #
    # p = figure(title="Reliability", x_axis_label='x', y_axis_label='y')
    # p.line(pointsX,cumulative,legend="Graph with failover",line_color="green")
    # #p.line(pointsX, pointsY_without_active_failover, legend="Graph without failover",line_color="orange")
    # output_file("reliability.html")
    # save(p)