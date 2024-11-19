function getGL(canvas){
	
	var gl = canvas.getContext("webgl")
	if(gl) return gl;
	
	var gl = canvas.getContext("experimental-webgl");
	if(gl) return gl;
	
	alert("WebGL unsupported in your browser. Update to a better one ;)");
	return false;
	
}

function createShader(gl, shaderType, shaderSrc){
	
	var shader = gl.createShader(shaderType);
	gl.shaderSource(shader, shaderSrc);
	gl.compileShader(shader);
	
	if(gl.getShaderParameter(shader, gl.COMPILE_STATUS)){
		return shader;
	}
	
	alert("Compile Error: " + gl.getShaderInfoLog(shader));
	
	gl.deleteShader(shader);
}

function createProgram(gl, vtxShader, fragShader){
	
	var prog = gl.createProgram();
	gl.attachShader(prog, vtxShader);
	gl.attachShader(prog, fragShader);
	gl.linkProgram(prog);
	
	if(gl.getProgramParameter(prog, gl.LINK_STATUS)){
		return prog;
	}
	
	alert("Linking Error: " + gl.getProgramInfoLog(prog));
	
	gl.deleteShader(prog);
	
}

function init(){
	var canvas = document.getElementById("glcanvas1");
	
	var gl = getGL(canvas);
	
	if(gl){
		
		var vtxShSrc = document.getElementById("vertex-shader").text;
		var fragShSrc = document.getElementById("frag-shader").text;
		
		var vtxShader = createShader(gl, gl.VERTEX_SHADER, vtxShSrc);
		var fragShader = createShader(gl, gl.FRAGMENT_SHADER, fragShSrc);
		var prog = createProgram(gl, vtxShader, fragShader);
		
		gl.useProgram(prog);
		
		var coordTriangle = new Float32Array([
											 -0.5,  0.5, 1.0, 0.0, 0.0, 1.0,
											 -0.5, -0.5, 0.0, 1.0, 0.0, 1.0,
											  0.5, -0.5, 1.0, 1.0, 0.0, 1.0,
											  0.5,  0.5, 0.0, 1.0, 1.0, 1.0,
											 -0.5,  0.5, 1.0, 0.0, 0.0, 1.0
											  ]);
		
		var bufPtr = gl.createBuffer();
		gl.bindBuffer(gl.ARRAY_BUFFER, bufPtr);
		gl.bufferData(gl.ARRAY_BUFFER, coordTriangle, gl.STATIC_DRAW);
		
		var positionPtr = gl.getAttribLocation(prog, "position");
		gl.enableVertexAttribArray(positionPtr);
		
		gl.vertexAttribPointer(positionPtr, 
							   2,        //Quantidade de dados/processamento
							   gl.FLOAT, //data type
							   false,	 //normalizar?
							   6*4, 		 //block size
							   0  		 //salto inicial
							  );
		
		var fcolorPtr = gl.getAttribLocation(prog, "fcolor");
		gl.enableVertexAttribArray(fcolorPtr);
		
		gl.vertexAttribPointer(fcolorPtr, 
							   4,        //Quantidade de dados/processamento
							   gl.FLOAT, //data type
							   false,	 //normalizar?
							   6*4, 		 //block size
							   2*4  		 //salto inicial
							  );
		
		
		gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
		gl.clearColor(0, 0, 0, 1);
		gl.clear(gl.COLOR_BUFFER_BIT);
		gl.enable(gl.BLEND);
		gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
		
		gl.drawArrays(gl.TRIANGLES, 0, 3);
		gl.drawArrays(gl.TRIANGLES, 2, 3);
	}

}