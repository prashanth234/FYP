import { ref } from "vue"
// import { useUserStore } from "@/stores/user";

export async function fetchImage(url: string) {
  // const user = useUserStore()
  // console.log(user.token)

  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': `JWT ${localStorage.getItem('fyptoken')}`
      }
    });
    const blob = await response.blob()
    return URL.createObjectURL(blob)
  } catch (error) {
    throw new Error('Error fetching image:', error);
  }
}
