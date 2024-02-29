import React, { useState } from 'react';
import axios from 'axios';
import '../css/register.css';
import { Link } from 'react-router-dom';

const Register = () => {
    const [showSuccessMessage, setShowSuccessMessage] = useState(false);
    const [showErrorMessage, setShowErrorMessage] = useState(false);
    const [formData, setFormData] = useState({
        user_name: '',  // Cambio aquí
        email: '',
        password: ''
    });

    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleRegistration = async (event) => {
        event.preventDefault();
    
        try {
            const response = await axios.post(
                'http://127.0.0.1:5000/user',
                formData,
                { 
                    withCredentials: true,  
                    headers: {
                        'Content-Type': 'application/json',  
                        'Access-Control-Allow-Origin': 'http://localhost:3000'  
                    }
                }
            );
            console.log(response.data); // Manejar la respuesta del backend según sea necesario
    
            setShowSuccessMessage(true);
            setTimeout(() => {
                setShowSuccessMessage(false);
            }, 3000);
        } catch (error) {
            console.error(error);
            setShowErrorMessage(true);
            setTimeout(() => {
                setShowErrorMessage(false);
            }, 3000);
        }
    };
    

    return (
        <>
            <section className='container'>
                <div className='login-container'>
                    <div className='form-container'>
                        <h1 className='titulo'>REGISTRARSE</h1>
                        <form onSubmit={handleRegistration}>
                            <input
                                type='text'
                                name='user_name'  // Cambio aquí
                                placeholder='USUARIO'
                                value={formData.user_name}  // Cambio aquí
                                onChange={handleInputChange}
                            />
                            <input
                                type='email'
                                name='email'
                                placeholder='EMAIL'
                                value={formData.email}
                                onChange={handleInputChange}
                            />
                            <input
                                type='password'
                                name='password'
                                placeholder='CONTRASEÑA'
                                value={formData.password}
                                onChange={handleInputChange}
                            />
                            <button className='opacity' type="submit">REGISTRARSE</button>
                        </form>
                        <div className='register-forget opacity'>
                            <Link to='/login' className='link'>INGRESAR</Link>
                        </div>
                    </div>
                </div>
            </section>
            {showSuccessMessage && (
                <div style={{
                    position: 'fixed',
                    bottom: '20px',
                    left: '20px',
                    backgroundColor: 'green',
                    color: 'white',
                    padding: '10px',
                    borderRadius: '5px',
                    zIndex: '9999'
                }}>
                    Usuario creado exitosamente
                </div>
            )}
            {showErrorMessage && (
                <div style={{
                    position: 'fixed',
                    bottom: '20px',
                    left: '20px',
                    backgroundColor: 'red',
                    color: 'white',
                    padding: '10px',
                    borderRadius: '5px',
                    zIndex: '9999'
                }}>
                    Ha ocurrido un error al crear el usuario
                </div>
            )}
        </>
    );
};

export default Register;
