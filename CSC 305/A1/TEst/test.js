var theta = [0,0,0];

function scale4(a, b, c) {
  var result = mat4();
  result[0][0] = a;
  result[1][1] = b;
  result[2][2] = c;
  return result;
}

window.onload = function init()
{
  var canvas = document.getElementById( "webgl-robot" );

  gl = WebGLUtils.setupWebGL( canvas );
  if ( !gl ) { alert( "WebGL isn't available" ); }

  gl.viewport( 0, 0, canvas.width, canvas.height );
  gl.clearColor( 1.0, 1.0, 1.0, 1.0 );
  gl.enable( gl.DEPTH_TEST ); 

  program = initShaders( gl, "vertex-shader", "fragment-shader" ); 
  gl.useProgram( program);

  colorCube();

  program = initShaders( gl, "vertex-shader", "fragment-shader" );    
  gl.useProgram( program );


  var vBuffer = gl.createBuffer();
  gl.bindBuffer( gl.ARRAY_BUFFER, vBuffer );
  gl.bufferData( gl.ARRAY_BUFFER, flatten(points), gl.DYNAMIC_DRAW );

  var vPosition = gl.getAttribLocation( program, "vPosition" );
  gl.vertexAttribPointer( vPosition, 4, gl.FLOAT, false, 0, 0 );
  gl.enableVertexAttribArray( vPosition );

  var cBuffer = gl.createBuffer();
  gl.bindBuffer( gl.ARRAY_BUFFER, cBuffer );
  gl.bufferData( gl.ARRAY_BUFFER, flatten(colors), gl.DYNAMIC_DRAW );

  var vColor = gl.getAttribLocation( program, "vColor" );
  gl.vertexAttribPointer( vColor, 4, gl.FLOAT, false, 0, 0 );
  gl.enableVertexAttribArray( vColor );

  modelView = gl.getUniformLocation( program, "modelView" );
  projection = gl.getUniformLocation( program, "projection" );

  document.getElementById("slider1").onchange = function() {
    theta[0] = event.srcElement.value;
  };
  document.getElementById("slider2").onchange = function() {
     theta[1] = event.srcElement.value;
  };
  document.getElementById("slider3").onchange = function() {
     theta[2] =  event.srcElement.value;
  };
  document.getElementById("slider4").onchange = function() {
     theta[3] = event.srcElement.value;
  };
  document.getElementById("slider5").onchange = function() {
     theta[4] = event.srcElement.value;
  };

  modelView2 = gl.getUniformLocation( program, "modelView" );
  projection2 = gl.getUniformLocation( program, "projection" );

  modelViewMatrixLoc = gl.getUniformLocation( program, "modelViewMatrix");
  projection = gl.getUniformLocation( program, "projection" );

  projectionMatrix = ortho(-10, 10, -10, 10, -10, 10);
  gl.uniformMatrix4fv( gl.getUniformLocation(program, "projectionMatrix"),  
  false, flatten(projectionMatrix) );

  render();
}

function base() {
   var s = scale4(BASE_WIDTH, BASE_HEIGHT, BASE_WIDTH);
   var instanceMatrix = mult( translate( 0.0, 0.5 * BASE_HEIGHT, 0.0 ), s);
   var t = mult(modelViewMatrix, instanceMatrix);
   gl.uniformMatrix4fv(modelViewMatrixLoc,  false, flatten(t) );
   gl.drawArrays( gl.TRIANGLES, 0, 36 );
}

function head() {
   var s = scale4(HEAD_WIDTH, HEAD_HEIGHT, HEAD_WIDTH);
   var instanceMatrix = mult(translate( 0.0, 0.5 * HEAD_HEIGHT, 0.0 ),s);    
   var t = mult(modelViewMatrix, instanceMatrix);
   gl.uniformMatrix4fv( modelViewMatrixLoc,  false, flatten(t) );
   gl.drawArrays( gl.TRIANGLES, 0, 36 );
}

function leftUpperArm()
{
   var s = scale4(LEFT_UPPER_WIDTH, LEFT_UPPER_HEIGHT, LEFT_UPPER_WIDTH);
   var instanceMatrix = mult( translate( 0.0, 0.5 * LEFT_UPPER_HEIGHT, 0.0 ), 
   s);
   var t = mult(modelViewMatrix, instanceMatrix);
   gl.uniformMatrix4fv( modelViewMatrixLoc,  false, flatten(t) );
   gl.drawArrays( gl.TRIANGLES, 0, 36 );
}

function leftLowerArm()
{
   var s = scale4(LEFT_LOWER_WIDTH, LEFT_LOWER_HEIGHT, LEFT_LOWER_WIDTH);
   var instanceMatrix = mult( translate( 0.0, 0.5 * LEFT_LOWER_HEIGHT, 0.0 ), 
    s);
   var t = mult(modelViewMatrix, instanceMatrix);
   gl.uniformMatrix4fv( modelViewMatrixLoc,  false, flatten(t) );
   gl.drawArrays( gl.TRIANGLES, 0, 36 );
}

function rightUpperArm()
{
   var s = scale4(RIGHT_UPPER_WIDTH, RIGHT_UPPER_HEIGHT, RIGHT_UPPER_WIDTH);
   var instanceMatrix = mult( translate( -9.3, 0.5 * RIGHT_UPPER_HEIGHT, 0.0 
   ), s);
   var t = mult(modelViewMatrix, instanceMatrix);
   gl.uniformMatrix4fv( modelViewMatrixLoc,  false, flatten(t) );
   gl.drawArrays( gl.TRIANGLES, 0, 36 );
}

function render() {

  gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT );

  modelViewMatrix = rotate(theta[Base], 0, 1, 0 );
  base();

  modelViewMatrix = mult(modelViewMatrix, translate(0.0, BASE_HEIGHT, 0.0)); 
  modelViewMatrix = mult(modelViewMatrix, rotate(theta[Head], 0, 0, 1 ));
  head();

  modelViewMatrix  = mult(modelViewMatrix, translate(1.3, -0.7, 0.0));
  modelViewMatrix  = mult(modelViewMatrix, rotate(theta[LeftUpper], 1, 0, 0) 
  );
  leftUpperArm();

  modelViewMatrix = mult(modelViewMatrix, translate(0.0, LEFT_UPPER_HEIGHT, 
  0.0));   
  modelViewMatrix = mult(modelViewMatrix, rotate(theta[LeftLower], 0, 0, 1 ));
  leftLowerArm();

  modelViewMatrix  = mult(modelViewMatrix, translate(5.3, -0.7, 0.0));
  modelViewMatrix  = mult(modelViewMatrix, rotate(theta[RightUpper], 1, 0, 0) 
  );
  rightUpperArm();

  requestAnimFrame(render);
}










"use strict";

var canvas;
var gl;

var numPositions  = 36;

var positions = [];
var colors = [];

var xAxis = 0;
var yAxis = 1;
var zAxis = 2;

var axis = 0;
var theta = [0, 0, 0];

var thetaLoc;

window.onload = function init()
{
    canvas = document.getElementById("gl-canvas");

    gl = canvas.getContext('webgl2');
    if (!gl) alert("WebGL 2.0 isn't available");

    colorCube();

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(1.0, 1.0, 1.0, 1.0);
    
   
    gl.enable(gl.DEPTH_TEST);

    //
    //  Load shaders and initialize attribute buffers
    //
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    var cBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

    var colorLoc = gl.getAttribLocation( program, "aColor" );
    gl.vertexAttribPointer( colorLoc, 4, gl.FLOAT, false, 0, 0 );
    gl.enableVertexAttribArray( colorLoc );

    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);


    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    thetaLoc = gl.getUniformLocation(program, "uTheta");

    //event listeners for buttons

    document.getElementById( "xButton" ).onclick = function () {
        axis = xAxis;
    };
    document.getElementById( "yButton" ).onclick = function () {
        axis = yAxis;
    };
    document.getElementById( "zButton" ).onclick = function () {
        axis = zAxis;
    };

    render();
}

function colorCube()
{
    quad(1, 0, 3, 2);
    quad(2, 3, 7, 6);
    quad(3, 0, 4, 7);
    quad(6, 5, 1, 2);
    quad(4, 5, 6, 7);
    quad(5, 4, 0, 1);
}

function quad(a, b, c, d)
{
    var vertices = [
        vec4(-0.5, -0.5,  0.5, 1.0),
        vec4(-0.5,  0.5,  0.5, 1.0),
        vec4(0.5,  0.5,  0.5, 1.0),
        vec4(0.5, -0.5,  0.5, 1.0),
        vec4(-0.5, -0.5, -0.5, 1.0),
        vec4(-0.5,  0.5, -0.5, 1.0),
        vec4(0.5,  0.5, -0.5, 1.0),
        vec4(0.5, -0.5, -0.5, 1.0)
    ];

    var vertexColors = [
        vec4(0.0, 0.0, 0.0, 1.0),  // black
        vec4(1.0, 0.0, 0.0, 1.0),  // red
        vec4(1.0, 1.0, 0.0, 1.0),  // yellow
        vec4(0.0, 1.0, 0.0, 1.0),  // green
        vec4(0.0, 0.0, 1.0, 1.0),  // blue
        vec4(1.0, 0.0, 1.0, 1.0),  // magenta
        vec4(0.0, 1.0, 1.0, 1.0),  // cyan
        vec4(1.0, 1.0, 1.0, 1.0)   // white
    ];

    // We need to parition the quad into two triangles in order for
    // WebGL to be able to render it.  In this case, we create two
    // triangles from the quad indices

    //vertex color assigned by the index of the vertex

    var indices = [a, b, c, a, c, d];

    for ( var i = 0; i < indices.length; ++i ) {
        positions.push( vertices[indices[i]] );
        //colors.push( vertexColors[indices[i]] );

        // for solid colored faces use
        colors.push(vertexColors[a]);
    }
}

function render()
{
    gl.clear( gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    theta[axis] += 2.0;
    gl.uniform3fv(thetaLoc, theta);

    gl.drawArrays(gl.TRIANGLES, 0, numPositions);
    requestAnimationFrame(render);
}