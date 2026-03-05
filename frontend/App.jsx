import React, { useState } from "react"
import axios from "axios"
import "./App.css"

export default function App(){

const [projectPath,setProjectPath] = useState("")
const [question,setQuestion] = useState("")
const [answer,setAnswer] = useState("")
const [loading,setLoading] = useState(false)

const ask = async ()=>{

if(!projectPath || !question) return

try{

setLoading(true)

const res = await axios.get("http://localhost:8000/analyze",{
params:{
project_path:projectPath,
question:question
}
})

setAnswer(res.data.answer)

}catch(err){

const detail = err.response?.data?.detail || err.message
setAnswer("Error: " + detail)

}

setLoading(false)

}

return(

<div className="app">

<div className="header">
<h1>AI Code Analyzer</h1>
</div>

<div className="main">

{/* LEFT PANEL */}

<div className="sidebar">

<h2>Project Setup</h2>

<label>Project Path</label>

<input
className="input"
placeholder="C:/my-project"
onChange={(e)=>setProjectPath(e.target.value)}
/>

<button className="primaryBtn" onClick={ask}>
{loading ? "Analyzing..." : "Start Analysis"}
</button>

</div>


{/* RIGHT PANEL */}

<div className="workspace">

<h2>Ask About Your Project</h2>

<textarea
className="questionBox"
placeholder="Ask anything about your codebase..."
onChange={(e)=>setQuestion(e.target.value)}
/>

<button className="analyzeBtn" onClick={ask}>
Analyze Project
</button>

<div className="answerPanel">

<h3>AI Response</h3>

<div className="answerText">
{answer || "Your AI response will appear here."}
</div>

</div>

</div>

</div>

</div>

)

}