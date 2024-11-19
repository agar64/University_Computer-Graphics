var texImg = [];
var texSrc = ["http://localhost:8080/neco_tr.png", "http://localhost:8080/rika_cat.png"];
var loadTexs = 0;
var gl;
var prog;
var df = 2.0;

var angle = 0;

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
	
	texImg[0] = new Image();
	texImg[0].src = texSrc[0];
	texImg[0].crossOrigin = "anonymous";
	texImg[0].onload = function(){
		loadTexs++;
		loadTextures();
	}
	
	texImg[1] = new Image();
	texImg[1].src = texSrc[1];
	texImg[1].crossOrigin = "anonymous";
	texImg[1].onload = function(){
		loadTexs++;
		loadTextures();
	}
	
}

function loadTextures(){
	if(loadTexs == texImg.length){
		initGL();
		configScene();
		draw();
	}
}

function initGL(){	
	var canvas = document.getElementById("glcanvas1");
	
	gl = getGL(canvas);
	
	if(gl){
		
		var vtxShSrc = document.getElementById("vertex-shader").text;
		var fragShSrc = document.getElementById("frag-shader").text;
		
		var vtxShader = createShader(gl, gl.VERTEX_SHADER, vtxShSrc);
		var fragShader = createShader(gl, gl.FRAGMENT_SHADER, fragShSrc);
		prog = createProgram(gl, vtxShader, fragShader);
		
		gl.useProgram(prog);
		
		//intialize drawing area, viewport, color, clears screen
		gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
		gl.clearColor(0, 0, 0, 1);
		gl.enable(gl.BLEND);
		gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
		
		gl.enable(gl.DEPTH_TEST);
		
		//gl.enable(gl.CULL_FACE);
		
	}
}

function configScene(){
		
	var coordTriangle = new Float32Array([
							//Quad 1
        					-0.5,  0.5, 0.0, 0.0, 0.0, 
        					-0.5, -0.5, 0.0, 0.0, 1.0, 
        					 0.5, -0.5, 0.0, 1.0, 1.0,
        					 0.5,  0.5, 0.0, 1.0, 0.0, 
        					-0.5,  0.5, 0.0, 0.0, 0.0,
        					
        					//Quad 2
        					-0.5, -0.5, 0.0, 1.0, 1.0, 
        					-0.5,  0.5, 0.0, 1.0, 0.0, 
        					-0.5,  0.5, 1.0, 0.0, 0.0,
        					-0.5, -0.5, 1.0, 0.0, 1.0, 
        					-0.5, -0.5, 0.0, 1.0, 1.0,
        					
        					//Quad 3
        					 0.5, -0.5, 1.0, 1.0, 1.0, 
        					 0.5, -0.5, 0.0, 1.0, 0.0, 
        					-0.5, -0.5, 0.0, 0.0, 0.0,
        					-0.5, -0.5, 1.0, 0.0, 1.0, 
        					 0.5, -0.5, 1.0, 1.0, 1.0
										  ]);
	
	var bufPtr = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, bufPtr);
	gl.bufferData(gl.ARRAY_BUFFER, coordTriangle, gl.STATIC_DRAW);
	
	var positionPtr = gl.getAttribLocation(prog, "position");
	gl.enableVertexAttribArray(positionPtr);
	
	gl.vertexAttribPointer(positionPtr, 
						   3,        //Quantidade de dados/processamento
						   gl.FLOAT, //data type
						   false,	 //normalizar?
						   5*4, 	 //block size
						   0  		 //salto inicial
						  );
	
	var texCoordPtr = gl.getAttribLocation(prog, "texCoord");
	gl.enableVertexAttribArray(texCoordPtr);
	
	gl.vertexAttribPointer(texCoordPtr, 
						   2,        //Quantidade de dados/processamento
						   gl.FLOAT, //data type
						   false,	 //normalizar?
						   5*4, 	 //block size
						   3*4  	 //salto inicial
						  );
	
	
	//send texture to GPU
	var tex0 = gl.createTexture();
	gl.activeTexture(gl.TEXTURE0);
	gl.bindTexture(gl.TEXTURE_2D, tex0);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
	gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texImg[0]);
	
	var tex1 = gl.createTexture();
	gl.activeTexture(gl.TEXTURE1);
	gl.bindTexture(gl.TEXTURE_2D, tex1);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
	gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
	gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, texImg[1]);
	
	dfPtr = gl.getUniformLocation(prog, "df");
	gl.uniform1f(dfPtr, df);
		
}

function draw(){
	
	var matrotZ = [Math.cos(angle*Math.PI/180.0), -Math.sin(angle*Math.PI/180.0), 0.0, 0.0,
				  Math.sin(angle*Math.PI/180.0),  Math.cos(angle*Math.PI/180.0), 0.0, 0.0,
				  0.0,    						0.0,   						 1.0, 0.0,
				  0.0,    						0.0,   						 0.0, 1.0];
	
	var matrotY = [Math.cos(angle*Math.PI/180.0), 0.0, -Math.sin(angle*Math.PI/180.0), 0.0,
				  0.0, 1.0, 0.0, 0.0,
				  Math.sin(angle*Math.PI/180.0), 0.0, Math.cos(angle*Math.PI/180.0), 0.0,
				  0.0,    						0.0,   						 0.0, 1.0];
	
	var matrotX = [1.0, 0.0, 0.0, 0.0,
				  0.0, Math.cos(angle*Math.PI/180.0), -Math.sin(angle*Math.PI/180.0), 0.0,
				  0.0, Math.sin(angle*Math.PI/180.0),  Math.cos(angle*Math.PI/180.0), 0.0,
				  0.0,    						0.0,   						 0.0, 1.0];
	
	rotXPtr = gl.getUniformLocation(prog, "rotX");
	gl.uniformMatrix4fv(rotXPtr, false, matrotX);
	
	rotYPtr = gl.getUniformLocation(prog, "rotY");
	gl.uniformMatrix4fv(rotYPtr, false, matrotY);
	
	rotZPtr = gl.getUniformLocation(prog, "rotZ");
	gl.uniformMatrix4fv(rotZPtr, false, matrotZ);
		
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
	
	//draw triangles
	var texPtr = gl.getUniformLocation(prog, "tex");
	gl.uniform1i(texPtr, 0);
	gl.drawArrays(gl.TRIANGLES, 0, 3);
	gl.drawArrays(gl.TRIANGLES, 2, 3);
	
	gl.uniform1i(texPtr, 1);
	gl.drawArrays(gl.TRIANGLES, 5, 3);
	gl.drawArrays(gl.TRIANGLES, 7, 3);
	
	gl.uniform1i(texPtr, 0);
	gl.drawArrays(gl.TRIANGLES, 10, 3);
	gl.uniform1i(texPtr, 1);
	gl.drawArrays(gl.TRIANGLES, 12, 3);
	
	angle++;
	
	requestAnimationFrame(draw);
}