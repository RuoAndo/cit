var blink = [];
var blink_bak = [];
var blink_bak_2 = [];
var blink_seq = [];

var counter = 0;

function LightsOut(id,columns,rows,cellsize){
    this.id = id;
    if(columns == undefined) columns = 5;
    if(rows == undefined) rows = 5;
    if(cellsize == undefined) cellsize = 50;
    this.size = cellsize;
    this.border = cellsize / 10;
    this.columns = columns;
    this.rows = rows;
    this.frame = document.getElementById(id);
    this.clickcount = [];
    this.lit = [];
    
    for(var y=0;y<this.rows;y++){
	this.clickcount[y] = [];
	this.lit[y] = [];
	for(var x=0;x<this.columns;x++){
	    this.clickcount[y][x] = 0;
	    this.lit[y][x] = 0;
	    var div = document.createElement('div');
	    div.id = this.id + String(y) + String(x);
	    div.style.width = this.size;;
	    div.style.height = this.size;
	    div.style.border = 'solid';
	    div.style.borderWidth = this.border;;
	    div.style.cssFloat = 'left'; // FF
	    div.style.styleFloat = 'left'; // IE
	    div.onmousedown = function(event){ click(event); };
	    div.lightsout = this;
	    this.frame.appendChild(div);
	}
	var br = document.createElement('br');
	br.clear = 'all';
	this.frame.appendChild(br);
    }
    this.display();    
}

LightsOut.prototype.toggle = function(x,y){
    if(x >= 0 && x < this.columns && y >= 0 && y < this.rows){
	this.lit[y][x] = (this.lit[y][x]+1) % 2;
    }
}

function click(ev){
    var x,y,e, tmp;
    if(ev) e = ev.target;
    if(! e) e = event.srcElement; // IE
    var lightsout = e.lightsout;

	// alert(e.lightsout);

    e.id.match(/(.)(.)$/);
    x = Number(RegExp.$2);
    y = Number(RegExp.$1);

    lightsout.toggle(x,y);
    lightsout.toggle(x+1,y);
    lightsout.toggle(x,y+1);
    lightsout.toggle(x-1,y);
    lightsout.toggle(x,y-1);

    lightsout.clickcount[y][x] = (lightsout.clickcount[y][x]+1) % 2;
    lightsout.display();
}

LightsOut.prototype.display = function(){

	if(counter==0)
	{
		//for(var y=0;y<9;y++)
    	//	blink[y] =0
    	for(var y=0;y<9;y++)
    		blink_bak[y] =0
    	for(var y=0;y<9;y++)
    		blink_bak_2[y] =0
    }

    for(var y=0;y<this.rows;y++){
	for(var x=0;x<this.columns;x++){
	    var e = document.getElementById(this.id+String(y)+String(x));
	    e.style.backgroundColor = (this.lit[y][x] == 1 ? 'blue' : 'yellow');
	    e.style.borderColor = (this.clickcount[y][x] == 1 ? '#ffccff' : '#ffffdd');
	}
    }

    for(var y=0;y<this.rows;y++){
	for(var x=0;x<this.columns;x++){
    	blink.push(this.lit[y][x]);
    }
    }
    
    for(var y=0;y<9;y++){
    	if(blink[y] != blink_bak_2[y])
    		blink_bak[y]=1
    	else
    		blink_bak[y]=0
    }
    
    if(counter > 0)
    {
    	for(var y=0;y<9;y++)
    		blink_seq.push(blink_bak_2[y]);
    	// blink_seq.reverse();
    	
    	blink_seq.push(" xor ")
    	
    	for(var y=0;y<9;y++)
    		blink_seq.push(blink_bak[y]);
    	// blink_seq.reverse();
    	
    	blink_seq.push("->")
    	
    	for(var y=0;y<9;y++)
    		blink_seq.push(blink[y]);
    	//blink_seq.reverse();
    	
    	blink_seq.push("<br>");
    }
    
    var getData = document.getElementById('getData');
    getData.innerHTML = blink;

    var getData2 = document.getElementById('getData2');
    getData2.innerHTML = blink_bak;
    
    var getData3 = document.getElementById('getData3');
    getData3.innerHTML = blink_bak_2;
    
    var getData4 = document.getElementById('getData4');
    getData4.innerHTML = blink_seq;

    for(var y=0;y<9;y++){
		blink_bak_2[y] = blink.pop();
	}
	
	blink_bak_2.reverse();
	
	counter = counter + 1;

}