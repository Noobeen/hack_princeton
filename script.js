// Set up the scene, camera, and renderer
let scene = new THREE.Scene();
let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

let renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("3d-container").appendChild(renderer.domElement);

// Load the logo texture
const loader = new THREE.TextureLoader();
loader.load('pprinceton.png', function(texture) {
    // Create a triangular geometry with the logo texture
    let geometry = new THREE.CircleGeometry(1, 3); // Triangle shape
    let material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.DoubleSide });
    let triangle = new THREE.Mesh(geometry, material);

    // Add the triangle to the scene
    scene.add(triangle);

    // Animation loop to rotate the triangle
    function animate() {
        requestAnimationFrame(animate);
        triangle.rotation.x += 0.01;
        triangle.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
});

// Resize renderer on window resize
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});