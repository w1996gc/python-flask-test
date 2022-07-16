var ec_right1 = echarts.init(document.getElementById('r1'), "dark");

var option_right1 = {

    backgroundColor: '#00008B',
    title: {
        text: '全国各地区城市确诊TOP10',
        textStyle: {
            color: 'white'
        },
        left: 'left'
    },
    color: ['#3398DB'],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function (value) {
                if (value == "地区待确认") {
                    value = "待确认"
                } else if (value == "境外输入") {
                    value = "境外"
                }
                return value.split("").join("\n");
            }
        }
    },
    yAxis: {
        type: 'value',
        //坐标轴刻度设置
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function (value) {
                if (value >= 1000) {
                    value = value / 1000 + 'k';
                }
                return value;
            }
        }
    },
    series: [{
        data: [],
        type: 'bar',
        barMaxWidth: "50%"
    }]
};
ec_right1.setOption(option_right1)
