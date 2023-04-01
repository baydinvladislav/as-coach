import { RootStore } from './RootStore';

export function actionLoading() {
  return (
    target: Record<string, any>,
    method: string,
    descriptor: PropertyDescriptor,
  ) => {
    const func = descriptor.value;

    descriptor.value = async function (...args: string[]) {
      if ('rootStore' in this) {
        const self = this as { rootStore: RootStore };
        let result;
        try {
          self.rootStore.loading.increaseLoadingStatus();
          result = await func.apply(this, args);
        } catch (e) {
          console.warn(e.message);
          throw e;
        } finally {
          self.rootStore.loading.decreaseLoadingStatus();
        }
        return result;
      }
      const name = target?.constructor?.name || '';
      console.warn(
        `decorator @actionLoading has no access to rootStore. [${name}@${method}]`,
      );
      return await func.apply(this, args);
    };
  };
}
