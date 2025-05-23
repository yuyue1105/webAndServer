document.getElementById('dataForm').addEventListener('submit',async function(e){
    e.preventDefault()
    const formData={
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
    
    };
    try{
        const response = await fetch('http://localhost:8000/api/submit' , {
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            boy:JSON.stringify(formData)
        })
        const data = await response.json();
        document.getElementById('response').innerHTML = `
            <p>服务器响应：</p>
            <p>状态：${data.status}</p>
            <p>消息：${data.message}</p>
            <p>接收到的数据:${JSON.stringify(data.receivedData)}</p>
        `;

        
    } catch (error){
        console.error('Error', error);
        document.getElementById('response').innerHTML = `
            <p style="color:red;">请求出错：${error.message}</p>
        `;
    }
})