
import * as THREE from 'https://unpkg.com/three/build/three.module.js';
import { GLTFLoader } from 'https://cdn.jsdelivr.net/npm/three@latest/examples/jsm/loaders/GLTFLoader.js';

document.addEventListener("DOMContentLoaded", function () {
    // Create a scene
    const scene = new THREE.Scene();

    // Create a camera
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    // Create a renderer
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById('model-container').appendChild(renderer.domElement);

    // Load the GLTF model
    const loader = new GLTFLoader();
    loader.load('static/model/t-shirt.gltf', (gltf) => {
        const model = gltf.scene;
        scene.add(model);
    });

    // Set the camera position
    camera.position.z = 5;

    // Animation function
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }

    // Start the animation
    animate();
});
