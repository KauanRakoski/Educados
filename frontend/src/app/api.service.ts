import { Injectable } from '@angular/core';
import axios, {AxiosInstance} from 'axios'

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private axiosInstance: AxiosInstance

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: "localhost:8000",
      headers: {
        "content-type": "application/json"
      }
    })
  }

  async get<T> (url: string): Promise<T>{
    try {
      let response = await axios.get(url)
      return response.data
    } catch(err){
      console.log("An error ocurred: ", err)
      throw err;
    }
  }
}
