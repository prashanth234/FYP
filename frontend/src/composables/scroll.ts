import { onIonViewWillLeave } from '@ionic/vue'
import { ref } from 'vue';

export function scrollTop() {
	const content = ref<any>(null)

	onIonViewWillLeave(() => {
		content.value && content.value.$el.scrollToTop()
	});

	return {
		content
	}
}