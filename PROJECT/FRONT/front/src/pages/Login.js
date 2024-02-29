import React, { useState } from 'react';
import '../css/login.css'
import { Link } from 'react-router-dom';

const Login = () => {

    return (
        <>
            <section className='container'>
                <div className='login-container'>
                    <div className='form-container'>
                        <h1 className='titulo'>LOGIN</h1>
                        <form>
                            <input type='text' placeholder='USUARIO'/>
                            <input type='text' placeholder='CONTRASEÑA'/>
                            <button className='opacity'>INGRESAR</button>
                        </form>
                        <div className='register-forget opacity'>
                            <Link to='/register' className='link'>No tienes cuenta? Regístrate</Link>
                        </div>
                    </div>
                </div>
            </section>
        </>
    )
}

export default Login