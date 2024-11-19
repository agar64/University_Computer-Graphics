var texImg = [];
var texSrc = ["http://localhost:8080/neco_tr.png", "http://localhost:8080/rika_cat.png"];
var loadTexs = 0;
var gl;
var prog;

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
	
	//Illumination
	var normals = new Float32Array([
        					//Quad 1
        					0, 0, 1,
        					0, 0, 1,
        					0, 0, 1,
        					0, 0, 1,
        					0, 0, 1,
        					
        					//Quad 2
        					1, 0, 0,
        					1, 0, 0,
        					1, 0, 0,
        					1, 0, 0,
        					1, 0, 0,
        					
        					//Quad 3
        					0, 1, 0,
        					0, 1, 0,
        					0, 1, 0,
        					0, 1, 0,
        					0, 1, 0
        									 ]);
        									
        var bufnormalPtr = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, bufnormalPtr);
        gl.bufferData(gl.ARRAY_BUFFER, normals, gl.STATIC_DRAW);
        
        var normalPtr = gl.getAttribLocation(prog, "normal");
        gl.enableVertexAttribArray(normalPtr);

        gl.vertexAttribPointer(normalPtr, 
        					   3,        
        					   gl.FLOAT, 
        					   false,    
        					   0,        
        					   0         
        					  );
        					  
        var lightDirectionPtr = gl.getUniformLocation(prog, "lightDirection");
        gl.uniform3fv(lightDirectionPtr, [0, 0, -1]/*[-0.2, -1, -0.7]*/);
        
        var lightColorPtr = gl.getUniformLocation(prog, "lightColor");
        gl.uniform3fv(lightColorPtr, [1, 1, 0]);
	
	
	
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
		
}

function createPerspective(fovY, aspectRatio, zNear, zFar){
	
	fovY = fovY*Math.PI/180.0;
	
	var fy = 1.0/math.tan(fovY/2);
	var fx = fy/aspectRatio;
	var B = -2*zFar*zNear/(zFar-zNear);
	var A = -(zFar+zNear)/(zFar-zNear);
	
	var proj = math.matrix(
							[[ fx, 0.0,  0.0, 0.0],
							 [0.0,  fy,  0.0, 0.0],
							 [0.0, 0.0,    A,   B],
							 [0.0, 0.0, -1.0, 0.0]]);
	return proj;
}

function createCamera(pos, target, up)
{  
  var zc = math.subtract(pos, target);
  zc = math.divide(zc, math.norm(zc));
  
  var yt = math.subtract(up, pos);
  yt = math.divide(yt, math.norm(yt));
  
  var xc = math.cross(yt, zc);
  xc = math.divide(xc, math.norm(xc));
  
  var yc = math.cross(zc, xc);
  yc = math.divide(yc, math.norm(yc));
  
  var mt = math.inv(math.transpose(math.matrix([xc,yc,zc])));
  
  mt = math.resize(mt, [4,4], 0);
  mt._data[3][3] = 1;
  
  var mov = math.matrix([[1, 0, 0, -pos[0]], 
                         [0, 1, 0, -pos[1]],
                         [0, 0, 1, -pos[2]],
                         [0, 0, 0, 1]]);
  
  var cam = math.multiply(mt, mov);
  
  return cam;
}

function draw(){
	
	var mproj = createPerspective(20, gl.canvas.width/gl.canvas.height, 1, 50);
	var cam = createCamera([5.0, 5.0, 5.0], [0.0, 0.0, 0.0], [5.0, 6.0, 5.0]);
	
	var tz = math.matrix(
							[[1.0, 0.0,  0.0,  0.0],
							 [0.0, 1.0,  0.0,  0.0],
							 [0.0, 0.0,  1.0, -5.0],
							 [0.0, 0.0,  0.0,  1.0]]);
	
	var matrotZ = math.matrix([[Math.cos(angle*Math.PI/180.0), -Math.sin(angle*Math.PI/180.0), 0.0, 0.0],
							   [Math.sin(angle*Math.PI/180.0),  Math.cos(angle*Math.PI/180.0), 0.0, 0.0],
							   [0.0,    						0.0,   						   1.0, 0.0],
							   [0.0,    						0.0,   						   0.0, 1.0]]);
	
	var matrotY = math.matrix([[Math.cos(angle*Math.PI/180.0), 0.0, -Math.sin(angle*Math.PI/180.0), 0.0],
							   [0.0, 						   1.0, 0.0, 							0.0],
							   [Math.sin(angle*Math.PI/180.0), 0.0, Math.cos(angle*Math.PI/180.0),  0.0],
							   [0.0,    					   0.0, 0.0,   							1.0]]);
	
	var matrotX = math.matrix([[1.0, 0.0, 							0.0, 							0.0],
							   [0.0, Math.cos(angle*Math.PI/180.0), -Math.sin(angle*Math.PI/180.0), 0.0],
							   [0.0, Math.sin(angle*Math.PI/180.0),  Math.cos(angle*Math.PI/180.0), 0.0],
							   [0.0, 0.0,   						0.0, 							1.0]]);
	
	var transform = math.multiply(matrotY, matrotX);
	transform = math.multiply(matrotZ, transform);
	transform = math.multiply(cam, transform);
	transform = math.multiply(mproj, transform);
	
	transfPtr = gl.getUniformLocation(prog, "transf");
	gl.uniformMatrix4fv(transfPtr, false, math.flatten(math.transpose(transform))._data);
		
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