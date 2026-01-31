import type {FC, ReactNode} from "react";
import cn from "classnames";
import cls from "./ButtonActive.module.scss"

interface ButtonActiveProps {
    appearance?: "primary" | "secondary";
    isLoading?: boolean;
    size?: "s" | "m" | "l";
    isBorder: boolean;
    children?: ReactNode;
}

export const ButtonActive:FC<ButtonActiveProps> = ({
                                                       children,
                                                       isLoading = false,
                                                       size = "m",
                                                       appearance = "primary",
                                                        isBorder = false
    }) => {
    return (
        <button
            type="button"
            disabled={isLoading}
            className={
            cn(cls.btn,
                cls[appearance],
                cls[size],
                {[cls.isLoading]: isLoading,
                    [cls.border]: isBorder
                })
            }>
                {children}
        </button>
    );
};

