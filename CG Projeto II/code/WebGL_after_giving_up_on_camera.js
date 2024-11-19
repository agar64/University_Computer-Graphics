var texImg = [];
var texSrc = ["http://localhost:8080/neco_tr.png", "http://localhost:8080/rika_cat.png"];
var loadTexs = 0;
var gl;
var prog;
var campos = [5, 5, 5]; //[5, 5, 5]
var lookAt = [0.0, 0.0, 0.0];
var camUp = math.add(campos, [0.0, 1.0, 0.0]); //[5.0, 6.0, 5.0]

var angle = 0;

var then = 0;
var deltaTime = 1;
var now = 0;

const keys = {};

var pause = false;
var once = true;
var onceScroll = true;

var mScroll = 0;

var speed = 5.0;
var scrollSpeed = 60.0;

var mainFOV = 20;

var firstDraw = true;

var xc = {};
var yc = {};
var zc = {};

var mattrans = math.matrix([[1.0, 0.0, 0.0, 0.0],
							    [0.0, 1.0, 0.0, 0.0],
							    [0.0, 0.0, 1.0, 0.0],
							    [0.0, 0.0, 0.0, 1.0]]);
	
var mattransY = mattrans;
var mattransZ = mattrans;
var mattransX = mattrans;

var moveMat = math.matrix(
							[[1.0, 0.0,  0.0,  0.0],
							 [0.0, 1.0,  0.0,  0.0],
							 [0.0, 0.0,  1.0,  0.0],
							 [0.0, 0.0,  0.0,  1.0]]);

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
        gl.uniform3fv(lightDirectionPtr, [0, 0, -1]/*[-0.2, -1, -0.7]*/); //0 0 -1
        
        var lightColorPtr = gl.getUniformLocation(prog, "lightColor");
        gl.uniform3fv(lightColorPtr, [1, 1, 1]);
		
		var lightposPtr = gl.getUniformLocation(prog, "lightpos");
        gl.uniform3fv(lightposPtr, [0.25, 0.0, 0.5]); //[0.5, 0.5, 0.25]
		
		var camposPtr = gl.getUniformLocation(prog, "campos");
        gl.uniform3fv(camposPtr, campos);
	
	
	
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
  if(firstDraw){
  
	zc = math.subtract(pos, target);
	zc = math.divide(zc, math.norm(zc));
  
	var yt = math.subtract(up, pos);
	yt = math.divide(yt, math.norm(yt));
  
	xc = math.cross(yt, zc);
	xc = math.divide(xc, math.norm(xc));
  
	yc = math.cross(zc, xc);
	yc = math.divide(yc, math.norm(yc));
	
	//firstDraw = false;
  }
  
  //[xc, zc, yc] = moveCam2(xc, zc, yc);
  
  //console.warn([xc, zc]);
  
  var mt = math.inv(math.transpose(math.matrix([xc,yc,zc])));
  
  mt = math.resize(mt, [4,4], 0);
  mt._data[3][3] = 1;
  
  var mov = math.matrix([[1, 0, 0, -pos[0]], 
                         [0, 1, 0, -pos[1]],
                         [0, 0, 1, -pos[2]],
                         [0, 0, 0, 1]]);
  
  //mov = moveCam3(mov);
  
  var cam = math.multiply(mt, mov);
  
  return cam;
}

function draw(now){
	
	var mproj = createPerspective(mainFOV, gl.canvas.width/gl.canvas.height, 1, 50);
	//var cam = createCamera([5.0, 5.0, 5.0], [0.0, 0.0, 0.0], [5.0, 6.0, 5.0]);
	var cam = createCamera(campos, lookAt, camUp);
	
	var tz = math.matrix(
							[[1.0, 0.0,  0.0,  0.0],
							 [0.0, 1.0,  0.0,  0.0],
							 [0.0, 0.0,  1.0,  -5.0], //-5
							 [0.0, 0.0,  0.0,  1.0]]);
	
	var transform = (tz, cam);
	var transformproj = math.multiply(mproj, transform);
	
	var transform = math.multiply(mattransY, mattransX);
	transform = math.multiply(mattransZ, transform);
	
	var transformproj = math.multiply(cam, transform); //moveCamNow
	transformproj = math.multiply(mproj, transformproj);
	
	[transformproj, transform] = animate(mproj, cam);
	//[transformproj, transform] = moveRotate(transformproj, transform);
	
	var transfprojPtr = gl.getUniformLocation(prog, "transfproj");
	gl.uniformMatrix4fv(transfprojPtr, false, math.flatten(math.transpose(transformproj))._data);
	
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
	
	if(!isNaN(deltaTime)) angle += 120.0*deltaTime; //impede o angle de virar NaN por algum motivo
	
	requestAnimationFrame(draw);
	
	now *= 0.001;
	deltaTime = now - then;
	then = now;
	
	move(transformproj);
	if(pause) deltaTime = 0; //se tiver pausado, dT = 0
	
	//alert(then);
}

function move(){ //eu deveria mudar isso pra case switch, mas agora estou com preguiça
	
	window.addEventListener('keydown', (e) => {
		keys[e.keyCode] = true;
		if(!(e.which || e.keyCode) == 116) e.preventDefault();
});
	window.addEventListener('keyup', (e) => {
		keys[e.keyCode] = false;
		e.preventDefault();
});

	gl.canvas.addEventListener('wheel', function(event){
		//console.log(event.deltaY);
		mScroll = event.deltaY;
		event.preventDefault()
		
	}, false);
	
	if(mScroll){
		if(onceScroll){
			const direction = mScroll/100;
			//console.warn(direction);
			//campos = math.add(campos, [0.0, deltaTime*scrollSpeed*direction, 0.0]);
			mainFOV += direction*scrollSpeed*deltaTime*0.1*mainFOV;
			if(mainFOV > 180) mainFOV = 180;
			if(mainFOV < 1) mainFOV = 1;
			//createPerspective(fovY, aspectRatio, zNear, zFar)
		}
		onceScroll = false; //scroll se comporta de forma estranha se eu deixar ele considerar múltiplos eventos por frame
		mScroll = 0.0;
	}else onceScroll = true;

	if (keys['104'] || keys['98']) {
		const direction = keys['104'] ? 1 : -1;
		campos = math.add(campos, [0.0, deltaTime*speed*direction, 0.0]);
	}
  
	if (keys['80']) {
	
		if(once) (!pause)?(pause = true):(pause = false); 
		//console.warn(pause);
		once = false; //sem isso, pausar se torna cara ou coroa
	
	}else once = true;
	
	if (keys['107'] || keys['109']) {
		const direction = keys['109'] ? 1 : -1;
		mainFOV += direction*speed*deltaTime*0.1*mainFOV;
		if(mainFOV > 180) mainFOV = 180; //desative para um efeito muito trippy
		if(mainFOV < 1) mainFOV = 1; //desative pra ficar preso com um FOV extremamente baixo
	}
	
	if (keys['38'] || keys['40']) {
		const direction = keys['38'] ? 1 : -1;
		lookAt = math.add(lookAt, [0.0, deltaTime*speed*direction, 0.0]);
	}
	
	if (keys['37'] || keys['39']) {
		const direction = keys['39'] ? 1 : -1;
		lookAt = math.add(lookAt, [0.5*deltaTime*speed*direction, 0.0, -0.5*deltaTime*speed*direction]);
	}
	
	if (keys['87'] || keys['83']) {
		const direction = keys['83'] ? 1 : -1;
		newcampos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, math.subtract(newcampos, campos));
		campos = newcampos;
		lookAt = math.add(lookAt, math.subtract(newcampos, campos));
	}
	
	if (keys['65'] || keys['68']) {
		const direction = keys['65'] ? 1 : -1;
		campos = math.add(campos, [deltaTime*speed*direction, 0.0, 0.0]);
	}
	
	//console.warn(lookAt);
  
	//console.warn(once);

}

/*
function moveCam(transform){
	
	if (keys['87'] || keys['83']) {
		const direction = keys['87'] ? 1 : -1;
		moveMat._data[2][3] = moveMat._data[2][3] + deltaTime*speed*direction;
		return transform = math.multiply(moveMat, transform);
		//campos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, [0.0, 0.0, deltaTime*speed*direction]);
	}
	
	return moveMat;
}
*/

function moveCam2(xc, zc, yc){
	
	if (keys['87'] || keys['83']) {
		const direction = keys['87'] ? 1 : -1;
		zc[0] = zc[0] + 0.1*deltaTime*speed*direction;
		zc[1] = zc[1] + 0.1*deltaTime*speed*direction;
		zc[2] = zc[2] + 0.1*deltaTime*speed*direction;
		return [xc, zc, yc];
		//campos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, [0.0, 0.0, deltaTime*speed*direction]);
	}
	
	if (keys['65'] || keys['68']) {
		const direction = keys['65'] ? 1 : -1;
		xc[0] = xc[0] + 0.2*deltaTime*speed*direction;
		xc[1] = xc[1] + 0.2*deltaTime*speed*direction;
		xc[2] = xc[2] + 0.2*deltaTime*speed*direction;
		//console.warn(math.transpose(math.matrix([xc,yc,zc])))
		return [xc, zc, yc];
		//campos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, [0.0, 0.0, deltaTime*speed*direction]);
	}
	
	return [xc, zc, yc];
}
/*
function moveCam3(mov){
	
	if (keys['87'] || keys['83']) {
		const direction = keys['87'] ? 1 : -1;
		mov._data[2][2] = mov._data[0][2] + deltaTime*speed*direction;
		return mov;
		//campos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, [0.0, 0.0, deltaTime*speed*direction]);
	}
	
	if (keys['65'] || keys['68']) {
		const direction = keys['65'] ? 1 : -1;
		mov._data[2][0] = mov._data[0][0] + deltaTime*speed*direction;
		//console.warn(math.transpose(math.matrix([xc,yc,zc])))
		return mov;
		//campos = math.add(campos, [0.0, 0.0, deltaTime*speed*direction]);
		//lookAt = math.add(lookAt, [0.0, 0.0, deltaTime*speed*direction]);
	}
	
	return mov;
}
*/

function animate(mproj, cam){
	
	var tz = math.matrix(
							[[1.0, 0.0,  0.0,  0.0],
							 [0.0, 1.0,  0.0,  0.0],
							 [0.0, 0.0,  1.0,  0.0], //-5
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
	/*
	var moveCamNow = moveCam(tz); //transform
	moveCamNow = math.multiply(tz, moveCamNow); //transform
	*/
	var transformproj = math.multiply(cam, transform); //moveCamNow
	transformproj = math.multiply(mproj, transformproj);
	
	return [transformproj, transform];
}

function moveRotate(transformproj, transform){
	
	
	
	return [transformproj, transform];
	
}