(function (window) {
    "use strict";
    var throttle = function (func, wait, options) {
        var context, args, result;
        var timeout = null;
        var previous = 0;
        if (!options) options = {};
        var later = function () {
            previous = options.leading === false ? 0 : new Date();
            timeout = null;
            result = func.apply(context, args);
            if (!timeout) context = args = null;
        };
        return function () {
            var now = new Date();
            if (!previous && options.leading === false) previous = now;
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0 || remaining > wait) {
                if (timeout) {
                    clearTimeout(timeout);
                    timeout = null;
                }
                previous = now;
                result = func.apply(context, args);
                if (!timeout) context = args = null;
            } else if (!timeout && options.trailing !== false) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    };
    var update_chart = function (chart, options) {
        chart.setOption(options);
    };
    var generate_chart_option = function (data,title) {
        var option = {
            title: { text: title },
            tooltip: { trigger: 'axis' },
            xAxis: {
                data: data.map(function (item) {
                    return item.index;
                })
            },
            yAxis: {
                splitLine: { show: false }
            },
            toolbox: {
                left: 'center',
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            },
            dataZoom: [{
                startValue: 0
            }, {
                type: 'inside'
            }],
            visualMap: {
                top: 2,
                right: -200,
                pieces: [{
                    gt: -0.5,
                    lte: 0.5,
                    color: '#096'
                    }, 
                    {
                        gt: -1,
                        lte: -0.5,
                        color: '#ffde33'
                    },
                    {
                        gt: 0.5,
                        lte: 1,
                        color: '#ffde33'
                    },
                    {
                        gt: -1.5,
                        lte: -1,
                        color: '#ff9933'
                    },
                    {
                        gt: 1,
                        lte: 1.5,
                        color: '#ff9933'
                    },
                    {
                        gt: -2,
                        lte: -1.5,
                        color: '#cc0033'
                    },
                    {
                        gt: 1.5,
                        lte: 2,
                        color: '#cc0033'
                    },
                    {
                        gt: 2,
                        lte: 3,
                        color: '#660099'
                    },
                    {
                        gt: -3,
                        lte: -2,
                        color: '#660099'
                    }],
                    outOfRange: {
                        color: '#999'
                    }
            },
            series: {
                name: 'Time Series',
                type: 'line',
                data: data.map(function (item) {
                    return item.value;
                }),
                // markLine: {
                //     silent: true,
                //     data: [{
                //         yAxis: 0.5
                //     }, {
                //         yAxis: -0.5
                //     }, {
                //         yAxis: -1
                //     }, {
                //         yAxis: 1
                //     }, {
                //         yAxis: -2
                //     }, {
                //         yAxis: 2
                //     },{
                //         yAxis: 1.5
                //     },{
                //         yAxis: -1.5
                //     }]
                // }
            }
        }
        return option;
    };


    var resize = function () {
        org_chart.resize();
        searched_chart.resize();
    };
    var org_chart;
    var searched_chart;
    var load = function () {
        org_chart = echarts.init(document.getElementById("canvas_origin"));
        searched_chart = echarts.init(document.getElementById("canvas_searched"));

        var div_org = document.getElementById("data_origin");
        var div_searched = document.getElementById("data_searched");

        var org_data = [];
        if(window.data.seq) {
            for(var i = 0; i < window.data.seq.length; i++) {
                org_data.push({
                    index: i,
                    value: window.data.seq[i]
                });
            }
        }
        var searched_data = [];
        if(window.data.query) {
            for(var i = 0; i < window.data.query.length; i++) {
                searched_data.push({
                    index: i,
                    value: window.data.query[i]
                });
            }
        }

        var org_options = generate_chart_option(org_data,"查询序列");
        var searched_options = generate_chart_option(searched_data,"最相似序列");
        update_chart(org_chart, org_options);
        update_chart(searched_chart, searched_options);

        div_org.remove();
        div_searched.remove();
    };

    window.addEventListener("load", load, false);
    window.addEventListener("resize", throttle(resize, 10), false);
})(window);