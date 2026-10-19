import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="MASHETI SYSTEM", layout="wide")

# --- PASTE YOUR HTML HERE ---
HTML_CODE = """
<!DOCTYPE html>
<html>
<head>
<title>MASHETI SYSTEM</title>
<style>
body { font-family: Arial; background: #f0f2f5; text-align: center; padding: 20px; }
.container { background: white; padding: 30px; border-radius: 15px; max-width: 800px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
h1 { color: #1e3a8a; }
button { background: #1e3a8a; color: white; padding: 12px 25px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
input { padding: 10px; width: 70%; border-radius: 8px; border: 1px solid #ccc; margin: 10px; }
</style>
</head>
<body>
<div class="container">
<h1>MASHETI SYSTEM V2</h1>
<p>Welcome to Masheti System - Now Live on Streamlit!</p>
<input type="text" id="nameInput" placeholder="Enter your name">
<br>
<button onclick="saveName()">Save Name</button>
<p id="result"></p>
<script>
function saveName(){
  var name = document.getElementById('nameInput').value;
  document.getElementById('result').innerHTML = "Hello " + name + " - Saved Successfully!";
  localStorage.setItem('masheti_name', name);
}
</script>
</div>
</body>
</html>
"""

components.html(HTML_CODE, height=800, scrolling=True)

st.success("✅ MASHETI SYSTEM is LIVE and working!")
