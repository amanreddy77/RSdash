import axios from "axios";
import * as actionTypes from '../Constants/vendorConstant';
// const URL = "http://localhost:8000";
const URL = "https://fooddelivery-xe7w.onrender.com";

export const getVendors = () => async (dispatch) => {
    try {
        const { data } = await axios.get(`${URL}/vendor/getVendors`);
        console.log('API Response:', data); // Check the response here
        dispatch({ type: actionTypes.Get_Vendors_Success, payload: data });
    } catch (e) {
        console.error('API Error:', e.message); // Log error details
        dispatch({ type: actionTypes.Get_Vendors_Failure, payload: e.message });
    }
};
