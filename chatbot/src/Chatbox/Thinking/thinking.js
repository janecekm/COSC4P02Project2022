import React from "react"
import { motion } from 'framer-motion';
import "./thinking.css"

const loadingCircle  = {
    display: 'block',
    width: '8px',
    height: '8px',
    backgroundColor: "whitesmoke",
    borderRadius: '15px'
}

const thinkingContainer = {
    display: "none",
    justifyContent: "space-around",
    width: "50px",
    marginTop:"3px",
    marginBottom:"2px",
    marginLeft: "5px",
    height: "25px",
    borderRadius: "10px"
}

const containerVariants = {
    start: {
        transition: {
            staggerChildren: 0.4
        }
    },
    end: {
        transition: {
            staggerChildren: 0.4
        }
    }
};

const circleVariants = {
    start: {
        y: '1%'
    },
    end: {
        y: "99%"
    }
};

const circleTransition = {
    ease: "easeInOut",
    duration: 0.6,
    yoyo: Infinity
}

export default function Thinking() {
    return (
    <motion.div 
        class = "cont"
        id = "think"
        style = {thinkingContainer} 
        variants = {containerVariants}
        initial="start"
        animate="end">
        <motion.span 
            style={loadingCircle} 
            variants = {circleVariants}
            transition = {circleTransition}
        ></motion.span>
        <motion.span 
            style={loadingCircle} 
            variants = {circleVariants}
            transition = {circleTransition}
        ></motion.span>
        <motion.span 
            style={loadingCircle} 
            variants = {circleVariants}
            transition = {circleTransition}
        ></motion.span>
    </motion.div>
    );
}