require('dotenv').config();

const mongoose = require('mongoose');

async function testConnection() {
    try {
        await mongoose.connect(process.env.MONGODB_URI, {
            serverSelectionTimeoutMS: 10000
        });

        console.log('MONGODB CONNECTED SUCCESSFULLY');
        await mongoose.disconnect();

    } catch (error) {
        console.log('MONGODB ERROR:', error.message);
        process.exitCode = 1;
    }
}

testConnection();