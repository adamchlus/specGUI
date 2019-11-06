
var margin = {top: 10, right: 20, bottom: 60, left: 60},
width = 800 - margin.left - margin.right,
height = 400 - margin.top - margin.bottom;
    
 
var dataIndex=1;
var sampling_interval = 10;
                
var yScale = d3.scaleLinear()
    .range([height,0]);
         
var xScale = d3.scaleLinear()
    .range([0,width]);
    
var xAxis = d3.axisBottom()
    .scale(xScale)
    .tickFormat(d3.format("0000"));

var yAxis = d3.axisLeft()
    .scale(yScale);

    
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    //xScale.domain([d3.min(data, function(d) { return d.wave; }), d3.max(data, function(d) { return d.wave; })]);
xScale.domain([387, 2505]);
    
//yScale.domain([0, d3.max(data, function(d) { return d.value; })]);  
yScale.domain([0, 40]);     
    
// text label for the x axis 
svg.append("text")             
    .attr("transform", "translate(" + (width/2) + " ," + (height + margin.top + 40) + ")")
    .style("text-anchor", "middle")
    .style("font-family","sans-serif")
    .style("font-size","18px")
    .text("Wavelength (nm)");
    
  svg.append("text")
      .attr("transform", "rotate(-90)") 
      .attr("y", 0 - margin.left) 
      .attr("x",0 - (height / 2))
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .style("font-family","sans-serif")
      .style("font-size","18px")
      .text("Reflectance");  
    
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .style("font-size","16px")
    .style('stroke-width', '5px') 
    .call(xAxis);

svg.append("g")
    .attr("class", "y axis")
    .style("font-size","16px")
    .style('stroke-width', '5px') 
    .call(yAxis);  
       
    updateData()
    

function updateData() {

    url =  "http://0.0.0.0:8000/data/spectra5.json";
    
    // request json from the server
    d3.json(url, function(error, data_json) {  
        
        var data = []; 

        //parse spectrum and color data
        for(var key in data_json[dataIndex]) { 
           data.push({wave: key, value:data_json[dataIndex][key],color:data_json[0][key] });
        } 
    
        console.log(data);    
        
var bar_width =  5;
 
   
var bar = svg.selectAll(".bar")
    .data(data);
        
    bar.enter().append("rect")
    .attr("class", "bar")
    .attr("height", function(d) { return height -2 - yScale(d.value); })
    .attr("width", bar_width)
    .attr("transform", function(d, i) { return "translate(" + xScale(d.wave - sampling_interval/2) + ","+ yScale(d.value) +")"; })
    .style("fill", function(d) { return d.color; })
    
   bar.exit().remove();  

            
    bar.transition()
    .duration(500)
    .ease(d3.easeQuad)
    .attr("height", function(d) { return height -2 - yScale(d.value); })
    .attr("width", bar_width)
    .style("fill", function(d) { return d.color; })
    .attr("transform", function(d, i) { return "translate(" + xScale(d.wave - sampling_interval/2) + ","+ yScale(d.value) +")"; });    
    
    console.log("test");      
    }); 
}
    

function next() {
    //sampling_interval = 10;
    dataIndex +=1;
    updateData();
        
}
    
function previous() {
    //sampling_interval = 10;
    dataIndex -=1;
    updateData();
        
}    










